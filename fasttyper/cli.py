from .application import Application
from .interface import Interface
from .components import (
    CursorComponent,
    StatsComponent,
    TextBox,
    TopMargin,
)
from .listener import Listener
from .buffer import UserBuffer, Buffer
from .config import Config
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

    reference_buffer = Buffer(rbuffer)
    user_buffer = UserBuffer()

    top_margin = TopMargin(config)
    cursor_component = CursorComponent(config)
    text_box = TextBox(config, cursor_component)
    stats_component = StatsComponent(config)

    listener = Listener(backspace_debug)
    application = Application(listener, user_buffer, reference_buffer, config)

    interface = Interface(
        application,
        [
            top_margin,
            text_box,
            stats_component,
            cursor_component,
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
        default="~/.config/fasttyper/config.json",
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
