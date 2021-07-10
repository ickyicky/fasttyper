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
