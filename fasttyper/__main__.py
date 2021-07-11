from .application import Application
from .interface import Interface
from .components import (
    UserInput,
    CursorComponent,
    ReferenceText,
    StatsComponent,
    TextBox,
)
from .listener import Listener
from .buffer import UserBuffer, Buffer
from .config import Config
from curses import wrapper
import sys
import io
import os
import argparse
import json


def initialize(configmap, rbuffer):
    config = Config(configmap)

    reference_buffer = Buffer(rbuffer)
    user_buffer = UserBuffer()

    cursor_component = CursorComponent(config)
    text_box = TextBox(config, cursor_component)
    user_input = UserInput(config, text_box)
    reference_text = ReferenceText(config, text_box)
    stats_component = StatsComponent(config)

    listener = Listener()
    application = Application(listener, user_buffer, reference_buffer, config)

    interface = Interface(
        application,
        [user_input, reference_text, text_box, stats_component, cursor_component],
    )
    wrapper(interface)

    application.summarize()


def main():
    is_tty = sys.stdin.isatty()

    parser = argparse.ArgumentParser()

    if is_tty:
        parser.add_argument("file", metavar="FILE", help="file to type")

    parser.add_argument(
        "--config",
        "-c",
        metavar="FILE",
        help="configuration file",
        default="~/.config/fasttyper/config.json",
    )
    args = parser.parse_args()

    if is_tty:
        with open(os.path.expanduser(args.file)) as f:
            rbuffer = f.read()
    else:
        input_lines = sys.stdin.readlines()

        with open("/dev/tty") as f:
            os.dup2(f.fileno(), 0)

        rbuffer = "".join(input_lines)

    try:
        with open(os.path.expanduser(args.config)) as f:
            configmap = json.load(f)
    except FileNotFoundError:
        configmap = {}

    initialize(configmap, rbuffer)


if __name__ == "__main__":
    main()
