from .cli import initialize, get_parser, RuntimeConfig
import sys
import os


def main():
    is_tty = sys.stdin.isatty()
    parser = get_parser()

    if is_tty:
        parser.add_argument("file", metavar="FILE", help="file to type")

    args = parser.parse_args()

    if is_tty:
        with open(os.path.expanduser(args.file)) as f:
            rbuffer = f.read()
    else:
        input_lines = sys.stdin.readlines()

        with open("/dev/tty") as f:
            os.dup2(f.fileno(), 0)

        rbuffer = "".join(input_lines)

    initialize(
        args.config,
        rbuffer,
        args.unclutter_backspace,
        args.no_cursor,
        RuntimeConfig(mode=RuntimeConfig.TEXT),
    )


if __name__ == "__main__":
    main()
