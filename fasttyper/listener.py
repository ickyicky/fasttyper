import enum
from .application import StoppingSignal


class Action(enum.Enum):
    add_char = "add_char"
    add_space = "add_space"
    add_newline = "add_newline"
    del_char = "del_char"
    del_word = "del_word"
    invalid = "invalid"


class Listener:
    def __init__(self):
        pass

    def handle_key(self, key):
        if key == "KEY_BACKSPACE":
            return Action.del_word, key
        elif key == chr(127):
            return Action.del_char, key
        elif key.startswith("KEY"):
            # special key pressed, or compbination
            return Action.invalid, key
        elif key == " ":
            return Action.add_space, key
        elif key == "\n":
            return Action.add_newline, key
        elif key.isprintable():
            return Action.add_char, key

        return Action.invalid, key

    def listen(self, screen):
        try:
            key = screen.getkey()
            return self.handle_key(key)
        except KeyboardInterrupt:
            raise StoppingSignal()
