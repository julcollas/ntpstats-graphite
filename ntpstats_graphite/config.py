#!/usr/bin/env python

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
