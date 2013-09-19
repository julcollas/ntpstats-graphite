#!/usr/bin/env python
from ntpstats_graphite import core
from optparse import OptionParser


def run():
    parser = OptionParser()
    parser.add_option('-P', '--path',
                      default='/var/log/ntpstats',
                      help="ntpstats directory, Default: %default")
    parser.add_option('-d', '--debug',
                      default='False', action='store_true',
                      help="Debug, Default: %default")
    parser.add_option('-p', '--prefix',
                      default='ntpstats',
                      help="Graphite prefix, Default: %default")

    (options, args) = parser.parse_args()

    core.process(path=options.path,
                 debug=options.debug,
                 prefix=options.prefix)