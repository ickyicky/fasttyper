from .listener import Action
from enum import Enum


class CharType(Enum):
    reference = 0
    valid = 1
    invalid = 2


class Buffer:
    def __init__(self, buffer, text_box, stats):
        self.reference_words = buffer.split()
        self.user_words = []

        self.total_words = len(self.reference_words)
        self.current_word = 0
        self.current_char = 0

        self.text_box = text_box
        self.stats = stats

        self.text_box.set_buffer(self)

    def _write(self, char):
        while self.current_word >= len(self.user_words):
            self.user_words.append("")

        valid = False
        try:
            valid = (
                self.reference_words[self.current_word][
                    len(self.user_words[self.current_word])
                ]
                == char
            )
        except IndexError:
            pass

        if valid:
            self.stats.signal_valid()
        else:
            self.stats.signal_invalid()

        self.user_words[self.current_word] += char
        self.current_char += 1

    def _next_word(self):
        self.current_word += 1
        self.current_char = 0
        self.stats.signal_valid()  # space is a char after all

    def _del_char(self):
        try:
            self.user_words[self.current_word] = self.user_words[self.current_word][:-1]
            self.current_char -= 1
            assert self.current_char >= 0
        except (IndexError, AssertionError):
            self.user_words = self.user_words[: self.current_word]
            self.current_word = max(0, self.current_word - 1)

            if self.current_word < len(self.user_words):
                self.current_char = len(self.user_words[self.current_word])
            else:
                self.current_char = 0

    def _del_word(self):
        try:
            self.user_words[self.current_word] = ""
            self.current_char = 0
        except IndexError:
            self.current_word = max(0, self.current_word - 1)

    def handle_action(self, action, char):
        if action == Action.add_char:
            self._write(char)
        elif action == Action.add_space:
            self._next_word()
        elif action == Action.del_char:
            self._del_char()
        elif action == Action.del_word:
            self._del_word()

        self.text_box.update_current_word(self.current_word)

    def get_word(self, index):
        reference_word = self.reference_words[index]
        user_word = ""

        try:
            user_word = self.user_words[index]
        except IndexError:
            pass

        word = [
            (r, CharType.valid if r == u else CharType.invalid)
            for r, u in zip(reference_word, user_word)
        ]
        word += [(c, CharType.invalid) for c in user_word[len(word) :]]
        word += [(c, CharType.reference) for c in reference_word[len(word) :]]

        return word
