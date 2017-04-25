#!/usr/bin/env python
from ntpstats_graphite import core
import click
import logging

@click.group()
@click.option('--debug/--no-debug',default=False,help='debugging output')
@click.option('--prefix',default="ntpstats",help="Graphite prefix")
@click.pass_context
def cli(ctx,debug,prefix):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    ctx.obj['prefix'] = prefix

@cli.command()
@click.option('--path',default="/var/log/ntpstats/",
               type=click.Path(exists=True,readable=True),
               help="Path to ntpstats directory")
@click.pass_context
def inotify(ctx,path,prefix):
    core.process(path=path,prefix=ctx.obj['prefix'])


def main():
    cli(obj={})

if __name__ == '__main__':
    main()
