from .application import Application
from .interface import Interface
from .components import (
    TextBox,
    Summary,
)
from .listener import Listener
from .buffer import Buffer
from .config import Config
from .stats import Stats
from curses import wrapper
import os
import argparse
import json


class RuntimeConfig:
    WORDS = "words"
    TEXT = "text"

    def __init__(self, words=None, language=None, mode=None):
        self.words = words
        self.language = language
        self.mode = mode


def initialize(config_path, rbuffer, backspace_debug, no_cursor, runtime_config):
    try:
        with open(os.path.expanduser(config_path)) as f:
            configmap = json.load(f)
    except FileNotFoundError:
        configmap = {}

    config = Config(configmap)

    text_box = TextBox(config)
    summary = Summary(config)
    stats = Stats(runtime_config)

    buffer = Buffer(rbuffer, text_box, stats)

    listener = Listener(backspace_debug)
    application = Application(listener, buffer, config)

    interface = Interface(
        application,
        [
            text_box,
        ],
        [
            summary,
        ],
        no_cursor,
    )
    wrapper(interface)

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
