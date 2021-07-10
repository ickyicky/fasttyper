from .application import Application
from .interface import Interface
from .components import UserInput, CursorComponent, ReferenceText, StatsComponent
from .listener import Listener
from .buffer import UserBuffer, Buffer
from curses import wrapper
import sys
import io
import os


def helpexit():
    print(
        "USAGE: fasttyper FILE or pipe text into fasttyper after executing 'exec 3<&0' in your shell"
    )
    sys.exit(1)


def main():
    if len(sys.argv) == 1:
        input_lines = sys.stdin.readlines()
        os.dup2(3, 0)
        rbuffer = io.StringIO("".join(input_lines))
    elif len(sys.argv) == 2:
        f = sys.argv[1]
        try:
            rbuffer = open(f)
        except:
            helpexit()
    else:
        helpexit()

    reference_buffer = Buffer(rbuffer)
    user_buffer = UserBuffer()

    cursor_component = CursorComponent()
    user_input = UserInput(cursor_component)
    reference_text = ReferenceText()
    stats_component = StatsComponent()

    listener = Listener()
    application = Application(listener, user_buffer, reference_buffer)

    interface = Interface(
        application,
        [user_input, reference_text, stats_component, cursor_component],
    )
    wrapper(interface)
    user_buffer.close()
    reference_buffer.close()

    stats = application.stats
    print(
        "\n".join(
            [
                f"WPM: {stats.correct_words / stats.total_minutes}",
                f"CPM: {stats.correct_chars / stats.total_minutes}",
                f"RAW WPM: {(stats.correct_words + stats.incorrect_words) / stats.total_minutes}",
                f"RAW CPM: {(stats.correct_chars + stats.incorrect_chars) / stats.total_minutes}",
                f"total seconds: {stats.total_seconds}",
                f"total minutes: {stats.total_minutes}",
                f"correct words: {stats.correct_words}",
                f"correct chars: {stats.correct_chars}",
                f"incorrect words: {stats.incorrect_words}",
                f"incorrect chars: {stats.incorrect_chars}",
                f"total words: {stats.incorrect_words + stats.correct_words}",
                f"total chars: {stats.incorrect_chars + stats.correct_chars}",
            ]
        )
    )


if __name__ == "__main__":
    main()
