import enum
import string
from .application import StoppingSignal


WHITE = [ord(c) for c in string.whitespace]
TAB = ord("\t")


class Action(enum.Enum):
    add_char = "add_char"
    add_space = "add_space"
    add_newline = "add_newline"
    del_char = "del_char"
    del_word = "del_word"
    invalid = "invalid"


class Listener:
    def __init__(self, backspace_debug=False):
        self.backspace_debug = not backspace_debug

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

        return Action.add_char

    def handle_key(self, key):
        action = Action.invalid

        if isinstance(key, str):
            key = ord(key)

        action = self.action_for_key(key)

        return action, chr(key)

    def listen(self, screen):
        try:
            key = screen.get_wch()
            return self.handle_key(key)
        except KeyboardInterrupt:
            raise StoppingSignal()
