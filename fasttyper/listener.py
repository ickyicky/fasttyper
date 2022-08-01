import os
import enum
import string
import curses
from .application import StoppingSignal


WHITE = [ord(c) for c in string.whitespace]
TAB = ord("\t")

TERMINALS_WITH_NORMAL_SPACE = [
    "xterm-kitty",
]


class Action(enum.Enum):
    add_char = "add_char"
    add_space = "add_space"
    add_newline = "add_newline"
    del_char = "del_char"
    del_word = "del_word"
    invalid = "invalid"


class Listener:
    def __init__(self, backspace_debug=False):
        self.backspace_debug = backspace_debug

        if os.environ.get("TERM", "") in TERMINALS_WITH_NORMAL_SPACE:
            self.backspace_debug = not self.backspace_debug

    def action_for_char(self, key):
        if key == "\t":
            raise StoppingSignal(silent=True)

        if ord(key) in (8, 127):
            return self.action_for_key(ord(key))

        if key in string.whitespace:
            return Action.add_space

        return Action.add_char

    def action_for_key(self, key):
        if (self.backspace_debug and key == 263) or (
            not self.backspace_debug and key == 127
        ):
            return Action.del_char

        if (self.backspace_debug and key == 8) or (
            not self.backspace_debug and key == 263
        ):
            return Action.del_word

        if key == TAB:
            raise StoppingSignal(silent=True)

        if key in WHITE:
            return Action.add_space

    def handle_key(self, key):
        action = Action.invalid

        if isinstance(key, str):
            action = self.action_for_char(key)
        else:
            action = self.action_for_key(key)
            key = chr(key)

        return action, key

    def listen(self, screen):
        try:
            key = screen.get_wch()
            return self.handle_key(key)
        except (KeyboardInterrupt, curses.error):
            raise StoppingSignal()
