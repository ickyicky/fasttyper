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


def get_config(config_path):
    try:
        with open(os.path.expanduser(config_path)) as f:
            configmap = json.load(f)
    except FileNotFoundError:
        configmap = {}

    config = Config(configmap)
    return config


def initialize(config, rbuffer, backspace_debug, no_cursor, runtime_config):
    if isinstance(config, str):
        config = get_config(config)

    backspace_debug = (
        backspace_debug(config) if callable(backspace_debug) else backspace_debug
    )
    no_cursor = no_cursor(config) if callable(no_cursor) else no_cursor

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
        default=ValueFromConfig("unclutter_backspace"),
    )
    parser.add_argument(
        "--no-cursor",
        "-n",
        action="store_true",
        help="disable cursos",
        default=ValueFromConfig("no_cursor"),
    )
    return parser


class ValueFromConfig:
    def __init__(self, key):
        self.key = key

    def __call__(self, config):
        return config.get(self.key)
