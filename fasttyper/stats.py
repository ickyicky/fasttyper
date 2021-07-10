from .listener import Action
from datetime import datetime


class Stats:
    def __init__(self):
        self.correct_words = 0
        self.correct_chars = 0
        self.incorrect_words = 0
        self.incorrect_chars = 0

        self.start_dtime = None
        self.stop_dtime = None

    def signal_running(self):
        if self.start_dtime is None:
            self.start_dtime = datetime.now()

    def update(self, action, valid):
        self.signal_running()

        if action == Action.add_char and valid is True:
            self.correct_chars += 1
        elif action == Action.add_char and valid is False:
            self.incorrect_chars += 1
        elif action in (Action.add_space, Action.add_newline) and valid is True:
            self.correct_chars += 1
            self.correct_words += 1
        elif action in (Action.add_space, Action.add_newline) and valid is False:
            self.incorrect_chars += 1
            self.incorrect_words += 1

    def signal_stop(self):
        self.stop_dtime = datetime.now()

    @property
    def total_seconds(self):
        stop_dtime = self.stop_dtime or datetime.now()
        start_dtime = self.start_dtime or datetime.now()
        return (stop_dtime - start_dtime).total_seconds() or 1

    @property
    def total_minutes(self):
        return self.total_seconds / 60

    @property
    def total_words(self):
        return self.incorrect_words + self.correct_words

    @property
    def total_chars(self):
        return self.incorrect_chars + self.correct_chars

    @property
    def wpm(self):
        return self.correct_words / self.total_minutes

    @property
    def cpm(self):
        return self.correct_chars / self.total_minutes

    @property
    def raw_wpm(self):
        return self.total_words / self.total_minutes

    @property
    def raw_cpm(self):
        return self.total_chars / self.total_minutes

    @property
    def accuracy(self):
        if self.total_chars:
            return self.correct_chars / self.total_chars * 100
        return 100
