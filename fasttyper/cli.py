from .application import Application
from .interface import Interface
from .components import (
    TextBox,
)
from .listener import Listener
from .buffer import Buffer
from .config import Config
from .stats import Stats
from curses import wrapper
import os
import argparse
import json


def initialize(config_path, rbuffer, backspace_debug, no_cursor):
    try:
        with open(os.path.expanduser(config_path)) as f:
            configmap = json.load(f)
    except FileNotFoundError:
        configmap = {}

    config = Config(configmap)

    text_box = TextBox(config)
    stats = Stats()

    buffer = Buffer(rbuffer, text_box, stats)

    listener = Listener(backspace_debug)
    application = Application(listener, buffer, config)

    interface = Interface(
        application,
        [
            text_box,
        ],
        no_cursor,
    )
    wrapper(interface)

    application.summarize()
    application.exit()


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        "-c",
        metavar="FILE",
        help="configuration file",
        default="~/.config/fasttyper/config_debug.json",
    )
    parser.add_argument(
        "--unclutter-backspace",
        "-b",
        action="store_true",
        help="unclutter backspace, when it raises ctrl+backspace instead",
        default=False,
    )
    parser.add_argument(
        "--no-cursor",
        "-n",
        action="store_true",
        help="disable cursos",
        default=False,
    )
    return parser
