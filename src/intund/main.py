import logging as log
import os
import os.path
import shutil
import sys
import time

import click

from . import bot
from . import gamestate
from . import overlay


DEF_LOG = 'intund.log'


def log_exception(extype, value, trace):
    """
    Hook to log uncaught exceptions to the logging framework. Register this as
    the excepthook with `sys.excepthook = log_exception`.
    """
    log.exception('Uncaught exception: ', exc_info=(extype, value, trace))


def setup_logging(log_file):
    """
    Sets up the logging framework to log to the given log_file and to STDOUT.
    If the path to the log_file does not exist, directories for it will be
    created.
    """
    if os.path.exists(log_file):
        backup = f'{log_file}.1'
        shutil.move(log_file, backup)

    term_handler = log.StreamHandler()
    handlers = [term_handler]

    fmt = '%(asctime)s %(levelname)-8s %(message)s'
    log.basicConfig(handlers=handlers, format=fmt, level=log.INFO)

    sys.excepthook = log_exception
    log.info('Started logging to: %s', log_file)


@click.group()
@click.option('--log-file', type=click.Path(dir_okay=False), default=DEF_LOG)
def cli(log_file):
    setup_logging(log_file)


@cli.command()
def play():
    player = bot.DksBot()
    player.play()


@cli.command()
@click.argument('pid', type=int)
def test_overlay(pid):
    state = gamestate.DksState(pid)
    over = overlay.Overlay(state)
    over.run()


if __name__ == '__main__':
    cli()
