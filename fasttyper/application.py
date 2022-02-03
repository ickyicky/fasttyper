import sys


class Application:
    def __init__(self, listener, user_buffer, reference_buffer, config):
        self.listener = listener
        self.user_buffer = user_buffer
        self.reference_buffer = reference_buffer
        self.config = config
        self.finished = False
        self.silent_exit = False

        from .state import StateMachine

        self.state = StateMachine(self)

        from .stats import Stats

        self.stats = Stats()

    def start(self):
        self.state.signal_start()

    def running(self):
        return self.state.running()

    def valid_user_text_position(self):
        if self.state.mistake_position is not None:
            return self.state.mistake_position
        return self.user_buffer.get_position()

    def get_user_text(self):
        text = self.user_buffer.get_matrix()
        mistake_position = self.valid_user_text_position()
        return text[:mistake_position], text[mistake_position:]

    def get_reference_text(self, position):
        return self.reference_buffer.get_matrix(position)

    def action(self, screen):
        try:
            action, key = self.listener.listen(screen)
            self.user_buffer.handle_action(action, key)
            self.state.update(action, key)
            self.stats.update(action, self.state.valid(), self.state.running())
        except StoppingSignal as e:
            self.state.signal_stop()
            self.stats.signal_stop()
            if e.silent:
                self.silent_exit = True

    def summarize(self):
        if self.finished:
            self.stats.summarize(self.config.get("summary_template"))
            self.stats.export_to_datafile(self.config.get("summary_datafile"))
            input()

    def exit(self):
        if self.finished or self.silent_exit:
            sys.exit(0)
        else:
            sys.exit(1)


class StoppingSignal(Exception):
    def __init__(self, *args, silent=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.silent = silent
