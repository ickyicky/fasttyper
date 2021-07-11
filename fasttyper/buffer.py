from .listener import Action


class Buffer:
    def __init__(self, buffer):
        self.buffer = " ".join(buffer.split())

    def _write(self, data):
        self.buffer += data

    def _del_char(self):
        self.buffer = self.buffer[:-1]

    def _last_char(self):
        if len(self.buffer) > 0:
            return self.buffer[-1]

    def _del_word(self):
        words = self.buffer.split()

        if len(words) > 1:
            self.buffer = " ".join(words[:-1]) + " "
        else:
            self.buffer = ""

    def handle_action(self, action, char):
        if action == Action.add_char:
            self._write(char)
        elif action == Action.add_space:
            self._write(" ")
        elif action == Action.add_newline:
            self._write("\n")
        elif action == Action.del_char:
            self._del_char()
        elif action == Action.del_word:
            self._del_word()

    def get_matrix(self, position=0):
        return self.buffer[position:]

    def get_position(self):
        return len(self.buffer)

    def get_lenght(self):
        return len(self.buffer)

    def read(self, position):
        return self.buffer[position]


class UserBuffer(Buffer):
    def __init__(self):
        super().__init__("")
