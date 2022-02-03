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
        self.tabbed = False

    def handle_key(self, key):
        action = Action.invalid

        if key == "\t":
            self.tabbed = True
        elif key == "\n" and self.tabbed:
            raise StoppingSignal()
        elif key == 263:
            action = Action.del_word
            self.tabbed = False
        elif isinstance(key, int):
            self.tabbed = False
        elif key == chr(127):
            action = Action.del_char
            self.tabbed = False
        elif key == " ":
            action = Action.add_space
            self.tabbed = False
        elif key == "\n":
            action = Action.add_newline
            self.tabbed = False
        elif key.isprintable():
            action = Action.add_char
            self.tabbed = False
        else:
            self.tabbed = False

        return action, key

    def listen(self, screen):
        try:
            key = screen.get_wch()
            return self.handle_key(key)
        except KeyboardInterrupt:
            raise StoppingSignal()
