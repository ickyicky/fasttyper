class Application:
    def __init__(self, listener, user_buffer, reference_buffer):
        self._running = False
        self.listener = listener
        self.user_buffer = user_buffer
        self.reference_buffer = reference_buffer

        from .state import StateMachine

        self.state = StateMachine(self)

        from .stats import Stats

        self.stats = Stats()

    def start(self):
        self._running = True

    def running(self):
        return self._running

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
            self.stats.update(action, self.state.valid())
        except StoppingSignal:
            self._running = False
            self.stats.signal_stop()


class StoppingSignal(Exception):
    pass
