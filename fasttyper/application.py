import sys
import readchar


class Application:
    def __init__(self, listener, buffer, config):
        self.listener = listener
        self.buffer = buffer
        self.config = config
        self.silent_exit = False

    @property
    def finished(self):
        return self.buffer.stats.finished

    def start(self):
        pass

    def running(self):
        return self.buffer.stats.running()

    def action(self, screen):
        try:
            action, key = self.listener.listen(screen)
            if self.running():
                self.buffer.handle_action(action, key)
            return True
        except StoppingSignal as e:
            if e.silent:
                self.silent_exit = True
            if self.running():
                self.buffer.stats.signal_stop()
            return False

    def summarize(self):
        if self.finished:
            self.buffer.stats.export_to_datafile(self.config.get("summary_datafile"))
            return True
        return False

    def exit(self):
        if not self.silent_exit:
            sys.exit(1)


class StoppingSignal(Exception):
    def __init__(self, *args, silent=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.silent = silent
