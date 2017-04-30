#!/usr/bin/env python
from ntpstats_graphite import core
import click
import logging
import os.path


@click.group()
@click.option('--debug/--no-debug', default=False, help='debugging output')
@click.option('--prefix', default='ntpstats', help='Graphite prefix')
@click.option('--server', default='localhost', help='carbon server address')
@click.option('--port', default=2003, help='carbon server port')
@click.pass_context
def cli(ctx, debug, prefix, server, port):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    ctx.obj['server'] = server
    ctx.obj['port'] = port
    ctx.obj['prefix'] = prefix


@cli.command()
@click.option(
    '--path', default='/var/log/ntpstats/',
    type=click.Path(exists=True, readable=True),
    help='Path to ntpstats directory'
)
@click.pass_context
def inotify(ctx, path, prefix):
    core.process(path=path, prefix=ctx.obj['prefix'])


@cli.command()
@click.option(
    '--loopstats', default='/var/log/ntpstats/loopstats',
    type=click.Path(exists=False, readable=True)
)
@click.option(
    '--peerstats', default='/var/log/ntpstats/peerstats',
    type=click.Path(exists=False, readable=True)
)
@click.option(
    '--rawstats', default='/var/log/ntpstats/rawstats',
    type=click.Path(exists=False, readable=True)
)
@click.option(
    '--sysstats', default='/var/log/ntpstats/sysstats',
    type=click.Path(exists=False, readable=True)
)
@click.pass_context
def oneshot(ctx, loopstats, peerstats, rawstats, sysstats):
    if os.path.exists(loopstats):
        with open(loopstats, 'r') as f:
            [core.loopstats(line, ctx.obj['prefix'], ctx.obj['server'], ctx.obj['port']) for line in f.readlines()]
    if os.path.exists(peerstats):
        with open(peerstats, 'r') as f:
            [core.peerstats(line, ctx.obj['prefix'], ctx.obj['server'], ctx.obj['port']) for line in f.readlines()]
    if os.path.exists(rawstats):
        with open(rawstats, 'r') as f:
            [core.rawstats(line, ctx.obj['prefix'], ctx.obj['server'], ctx.obj['port']) for line in f.readlines()]
    if os.path.exists(sysstats):
        with open(sysstats, 'r') as f:
            [core.sysstats(line, ctx.obj['prefix'], ctx.obj['server'], ctx.obj['port']) for line in f.readlines()]


def main():
    cli(obj={})

if __name__ == '__main__':
    main()
