#!/usr/bin/env python
from ntpstats_graphite import config
import pyinotify
import datetime
import calendar
import socket


def mjd_to_timestamp(mjd, pastmidnight):
    '''Convert ntp MJD time to unix timestamp'''
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    date = midnight + datetime.timedelta(0, float(pastmidnight))
    timestamp = calendar.timegm(date.timetuple())
    return timestamp


def get_peer_tallycode(statusWord):
    '''Get the tally code from the Peer Status Word
    ref: http://www.eecis.udel.edu/~mills/ntp/html/decode.html'''
    sw_hex = int(statusWord, 16)
    sw_bin = bin(sw_hex)[2:]
    sw_tally = sw_bin[5:8]
    tally_bin = int(sw_tally, 2)
    return tally_bin


def stats_to_dict(string, input_list):
    '''Return a dict from a single ntpstats line and a matching list'''
    ret_val = False
    if len(string.split(' ')) == len(input_list):
        ret_val = dict(zip(input_list, string.split(' ')))
    return ret_val


def dict_to_carbon(stats_dict, prefix, debug):
    '''Return a formated carbon input from a dict and prefix'''
    date = stats_dict.pop('date')
    timePastMidnight = stats_dict.pop('timePastMidnight')
    timestamp = mjd_to_timestamp(date, timePastMidnight)

    lines = []
    for item in stats_dict:
        metric = '.'.join([prefix, item])
        lines.append('%s %s %s' % (metric, stats_dict[item], timestamp))

    if debug is True:
        print '\n'.join(lines) + '\n'
    return lines


def send_msg(message):
    '''Send message to carbon'''
    sock = socket.socket()
    sock.connect((config.CARBON_SERVER, int(config.CARBON_PORT)))
    sock.sendall(message)
    sock.close()


def loopstats(string, prefix, debug):
    '''Parse loopstats statistics'''
    prefix += '.loopstats'
    loopstats_dict = stats_to_dict(string, config.loopstats_list)
    to_send = dict_to_carbon(loopstats_dict, prefix, debug)
    send_msg('\n'.join(to_send) + '\n')


def peerstats(string, prefix, debug):
    '''Parse peerstats statistics'''
    peerstats_dict = stats_to_dict(string, config.peerstats_list)
    tallycode = get_peer_tallycode(peerstats_dict['statusWord'])
    peerstats_dict['statusWord'] = tallycode
    peer = peerstats_dict.pop('sourceAddress').replace('.', '-')
    prefix += '.' + '.'.join(['peerstats', peer])
    to_send = dict_to_carbon(peerstats_dict, prefix, debug)
    send_msg('\n'.join(to_send) + '\n')


def rawstats(string, prefix, debug):
    '''Parse rawstats statistics'''
    rawstats_dict = stats_to_dict(string, config.rawstats_list)
    rawstats_dict.pop('destinationAddress')
    source = rawstats_dict.pop('sourceAddress').replace('.', '-')
    prefix += '.' + '.'.join(['rawstats', source])
    to_send = dict_to_carbon(rawstats_dict, prefix, debug)
    send_msg('\n'.join(to_send) + '\n')


def sysstats(string, prefix, debug):
    '''Parse sysstats statistics'''
    prefix += '.sysstats'
    sysstats_dict = stats_to_dict(string, config.sysstats_list)
    to_send = dict_to_carbon(sysstats_dict, prefix, debug)
    send_msg('\n'.join(to_send) + '\n')


class EventProcessor(pyinotify.ProcessEvent):

    def __init__(self, prefix, debug):
        self.prefix = prefix
        self.debug = debug

    def process_IN_MODIFY(self, event):
        self.file = open(event.pathname)
        lines = self.file.readlines()
        lastline = lines[-1].rstrip()

        if 'loopstats' in event.pathname:
            loopstats(lastline, self.prefix, self.debug)

        elif 'peerstats' in event.pathname:
            peerstats(lastline, self.prefix, self.debug)

        elif 'rawstats' in event.pathname:
            rawstats(lastline, self.prefix, self.debug)

        elif 'sysstats' in event.pathname:
            sysstats(lastline, self.prefix, self.debug)


def process(path, prefix, debug):
    wm = pyinotify.WatchManager()
    handler = EventProcessor(prefix, debug)
    wm.add_watch(path, pyinotify.IN_MODIFY, rec=True)
    notifier = pyinotify.Notifier(wm, handler)
    notifier.loop()
