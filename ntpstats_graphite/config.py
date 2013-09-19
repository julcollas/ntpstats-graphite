#!/usr/bin/env python
from os import environ

CARBON_SERVER = (environ.get('CARBON_SERVER') or 'localhost')
CARBON_PORT = (environ.get('CARBON_PORT') or 2003)

loopstats_list = [
    'date',
    'timePastMidnight',
    'clockOffset',
    'frequencyOffset',
    'rmsJitter',
    'rmsFrequencyJitter',
    'clockDisciplineLoopTimeConstant'
]


peerstats_list = [
    'date',
    'timePastMidnight',
    'sourceAddress',
    'statusWord',
    'clockOffset',
    'roundtripDelay',
    'dispersion',
    'rmsJitter'
]


rawstats_list = [
    'date',
    'timePastMidnight',
    'sourceAddress',
    'destinationAddress',
    'originTimestamp',
    'receiveTimestamp',
    'transmitTimestamp',
    'destinationTimestamp'
]


sysstats_list = [
    'date',
    'timePastMidnight',
    'timeSinceReset',
    'packetsReceived',
    'packetForThisHost',
    'currentVersions',
    'oldVersion',
    'badVersion',
    'accessDenied',
    'badLenghtOrFormat',
    'badAuthentication',
    'rateExceeded',
]