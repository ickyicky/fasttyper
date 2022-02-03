import enum
from .listener import Action
from .application import StoppingSignal


class State(enum.Enum):
    valid = "valid"
    invalid = "invalid"
    finished = "finished"


class StateMachine:
    def __init__(self, application):
        self.state = State.valid
        self.mistake_position = None
        self.application = application

    def running(self):
        return self.state != State.finished

    def signal_stop(self):
        self.state = State.finished

    def signal_start(self):
        self.state = State.valid
        self.mistake_position = None

    def update(self, action, char):
        user_position = self.application.user_buffer.get_position()
        if self.state == State.invalid:
            if action in (Action.del_char, Action.del_word):
                if user_position <= self.mistake_position:
                    self.mistake_position = None
                    self.state = State.valid
        if self.state == State.valid:
            if action in (Action.add_char, Action.add_space, Action.add_newline):
                if char != self.application.reference_buffer.read(user_position - 1):
                    self.mistake_position = user_position - 1
                    self.state = State.invalid
                elif user_position == self.application.reference_buffer.get_lenght():
                    self.state = State.finished
                    self.application.finished = True

    def valid(self):
        return self.state in (State.valid, State.finished)
