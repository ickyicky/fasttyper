import io
from .listener import Action


class Buffer:
    def __init__(self, buffer):
        self.buffer = buffer
        self._strip_end()

    def _write(self, data):
        self.buffer.write(data)

    def _del_char(self):
        pos = self.buffer.tell()

        if pos > 0:
            self.buffer.seek(pos - 1)
            self.buffer.truncate()
            return True

    def _last_char(self):
        pos = self.buffer.tell()

        if pos > 0:
            self.buffer.seek(pos - 1)
            return self.buffer.read(1)

    def _del_word(self):
        found_word = False

        while True:
            last_char = self._last_char()

            if last_char is None:
                break

            if last_char in (" ", "\n") and found_word:
                break

            if last_char.isalnum() and not found_word:
                found_word = True

            self._del_char()

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
        self.buffer.seek(position)
        return self.buffer.read()

    def get_position(self):
        return self.buffer.tell()

    def get_lenght(self):
        position = self.get_position()
        self.buffer.read()
        lenght = self.get_position()
        self.buffer.seek(position)
        return lenght

    def read(self, position):
        _position = self.get_position()
        self.buffer.seek(position)
        char = self._last_char()
        self.buffer.seek(_position)
        return char

    def close(self):
        self.buffer.close()

    def _strip_end(self):
        self.buffer.read()
        while True:
            last_char = self._last_char()

            if last_char is None:
                break

            if last_char.isalnum():
                break

            self._del_char()
        self.buffer.seek(0)


class UserBuffer(Buffer):
    def __init__(self):
        super().__init__(io.StringIO())
