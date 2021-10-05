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
        action = Action.invalid

        if key == 263:
            action = Action.del_char  # TODO
        elif isinstance(key, int):
            pass
        elif key == chr(127):
            action = Action.del_char
        elif key == " ":
            action = Action.add_space
        elif key == "\n":
            action = Action.add_newline
        elif key.isprintable():
            action = Action.add_char

        return action, key

    def listen(self, screen):
        try:
            key = screen.get_wch()
            return self.handle_key(key)
        except KeyboardInterrupt:
            raise StoppingSignal()
