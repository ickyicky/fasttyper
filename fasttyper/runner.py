from .cli import initialize, get_parser, RuntimeConfig
from random import choice
import os
import requests
import pathlib


MONKEYTYPE_WORDS_PATT = "https://raw.githubusercontent.com/Miodec/monkeytype/master/frontend/static/languages/{language}.json"


def get_words(language):
    home = os.environ.get("HOME", "")
    sfile = os.path.join(home, ".cache", "fasttyper", language)
    words = None

    try:
        with open(sfile) as f:
            words = f.read().splitlines()
    except FileNotFoundError:
        pass

    if words is None:
        source_path = MONKEYTYPE_WORDS_PATT.format(language=language)

        words = requests.get(source_path).json()["words"]

        p = pathlib.Path(os.path.join(home, ".cache", "fasttyper"))
        p.mkdir(parents=True, exist_ok=True)

        with open(sfile, "w") as f:
            f.write("\n".join(words))

    return words


def runner():
    parser = get_parser()

    parser.add_argument(
        "amount", type=int, default=25, help="Amount of words", nargs="?"
    )
    parser.add_argument(
        "language", type=str, default="english", help="Language", nargs="?"
    )

    args = parser.parse_args()
    words = get_words(args.language)

    while True:
        rbuffer = " ".join([choice(words) for _ in range(args.amount)])
        initialize(
            args.config,
            rbuffer,
            args.unclutter_backspace,
            args.no_cursor,
            RuntimeConfig(
                mode=RuntimeConfig.WORDS, words=args.amount, language=args.language
            ),
        )


if __name__ == "__main__":
    runner()
