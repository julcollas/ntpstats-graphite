#! /usr/bin/env python
from setuptools import setup, find_packages

# Extracts the __version__
VERSION = [l for l in open('ntpstats_graphite/__init__.py').readlines()
           if l.startswith('__version__ = ')][0].split("'")[1]

setup(
    name='ntpstats-graphite',
    version=VERSION,
    packages=find_packages(),
    description='Send ntpstats to Graphite',
    keywords='ntp graphite',
    author='Julien',
    entry_points={
        'console_scripts': ['ntpstats-graphite-poller = ntpstats_graphite.cli:main']
    },
    install_requires=['pyinotify', 'click'],
)
