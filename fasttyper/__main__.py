from .application import Application
from .interface import Interface
from .components import UserInput, CursorComponent, ReferenceText, StatsComponent
from .listener import Listener
from .buffer import UserBuffer, Buffer
from .config import Config
from curses import wrapper
import sys
import io
import os
import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", metavar="FILE", nargs="?")
    parser.add_argument(
        "--config",
        "-c",
        metavar="FILE",
        help="configuration file",
        default="~/.config/fasttyper/config.json",
    )
    args = parser.parse_args()

    if args.file is None:
        input_lines = sys.stdin.readlines()
        os.dup2(3, 0)
        rbuffer = io.StringIO("".join(input_lines))
    else:
        with open(args.file) as f:
            rbuffer = io.StringIO(f.read())

    try:
        with open(args.config) as f:
            configmap = json.load(f)
    except FileNotFoundError:
        configmap = {}

    config = Config(configmap)

    reference_buffer = Buffer(rbuffer)
    user_buffer = UserBuffer()

    cursor_component = CursorComponent()
    user_input = UserInput(cursor_component)
    reference_text = ReferenceText()
    stats_component = StatsComponent()

    listener = Listener()
    application = Application(listener, user_buffer, reference_buffer, config)

    interface = Interface(
        application,
        [user_input, reference_text, stats_component, cursor_component],
    )
    wrapper(interface)
    user_buffer.close()
    reference_buffer.close()

    print(config.get("summary_template").format(stats=application.stats))


if __name__ == "__main__":
    main()
