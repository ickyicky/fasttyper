from .cli import initialize, get_parser, RuntimeConfig, get_config, ValueFromConfig
from random import choice, random
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


def generate_text(
    words,
    amount,
    capitalization_factor,
    punctuation_factor,
    sentence_mode,
    punctuation,
    sentence_ending,
):
    chosen_words = []

    new_sentence = True
    for _ in range(amount):
        word = choice(words)

        if sentence_mode and new_sentence:
            word = word.capitalize()
            new_sentence = False
        elif capitalization_factor and capitalization_factor / 100 > random():
            word = word.capitalize()

        if punctuation_factor and punctuation_factor / 100 > random():
            punctuation = choice(punctuation)
            word = "".join((word, punctuation))

        new_sentence = word[-1] in sentence_ending
        chosen_words.append(word)

    return " ".join(chosen_words)


def runner():
    parser = get_parser()

    parser.add_argument(
        "amount",
        type=int,
        default=ValueFromConfig("amount"),
        help="Amount of words",
        nargs="?",
    )
    parser.add_argument(
        "language",
        type=str,
        default=ValueFromConfig("language"),
        help="Language",
        nargs="?",
    )
    parser.add_argument(
        "-rc",
        "--random-capitalization",
        type=int,
        default=ValueFromConfig("random_capitalization"),
        help="Percent of randomally capitalized words",
        action="store",
    )
    parser.add_argument(
        "-rp",
        "--random-punctuation",
        type=int,
        default=ValueFromConfig("random_capitalization"),
        help="Percent of words that will have randomally appender punctuation at the end",
        action="store",
    )
    parser.add_argument(
        "-sm",
        "--sentence-mode",
        default=ValueFromConfig("sentence_mode"),
        help="Forces uppercase after sentence ending characters like dot or question mark and at the beggining of text",
        action="store_true",
    )
    parser.add_argument(
        "--punctuation",
        type=str,
        default=ValueFromConfig("punctuation"),
        help="List of all punctuation characters",
        action="store",
    )
    parser.add_argument(
        "--sentence-ending",
        type=str,
        default=ValueFromConfig("sentence_ending"),
        help="List of all punctuation characters that end sentence",
        action="store",
    )

    args = parser.parse_args()
    config = get_config(args.config)

    random_punctuation = (
        args.random_punctuation(config)
        if callable(args.random_punctuation)
        else args.random_punctuation
    )
    random_capitalization = (
        args.random_capitalization(config)
        if callable(args.random_capitalization)
        else args.random_capitalization
    )
    sentence_mode = (
        args.sentence_mode(config)
        if callable(args.sentence_mode)
        else args.sentence_mode
    )
    punctuation = (
        args.punctuation(config) if callable(args.punctuation) else args.punctuation
    )
    sentence_ending = (
        args.sentence_ending(config)
        if callable(args.sentence_ending)
        else args.sentence_ending
    )
    amount = args.amount(config) if callable(args.amount) else args.amount
    language = args.language(config) if callable(args.language) else args.language

    words = get_words(language)

    while True:
        rbuffer = generate_text(
            words,
            amount,
            random_capitalization,
            random_punctuation,
            sentence_mode,
            punctuation,
            sentence_ending,
        )
        initialize(
            config,
            rbuffer,
            args.unclutter_backspace,
            args.no_cursor,
            RuntimeConfig(
                mode=RuntimeConfig.WORDS, words=args.amount, language=args.language
            ),
        )


if __name__ == "__main__":
    runner()
