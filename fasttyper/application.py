import sys
import readchar


class Application:
    def __init__(self, listener, buffer, config):
        self.listener = listener
        self.buffer = buffer
        self.config = config
        self.finished = False
        self.silent_exit = False

    def start(self):
        pass

    def running(self):
        return True

    def action(self, screen):
        try:
            action, key = self.listener.listen(screen)
            self.buffer.handle_action(action, key)
        except StoppingSignal as e:
            if e.silent:
                self.silent_exit = True

    def summarize(self):
        if self.finished:
            self.buffer.stats.summarize(self.config.get("summary_template"))
            self.buffer.stats.export_to_datafile(self.config.get("summary_datafile"))
            try:
                readchar.readchar()
            except KeyboardInterrupt:
                sys.exit(1)

    def exit(self):
        if not self.finished and not self.silent_exit:
            sys.exit(1)


class StoppingSignal(Exception):
    def __init__(self, *args, silent=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.silent = silent
