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
            self.buffer.handle_action(action, key)
        except StoppingSignal as e:
            if e.silent:
                self.silent_exit = True
            self.buffer.stats.signal_stop()

    def summarize(self):
        if self.finished:
            self.buffer.stats.summarize(self.config.get("summary_template"))
            self.buffer.stats.export_to_datafile(self.config.get("summary_datafile"))
            try:
                c = readchar.readchar()
                if ord(c) == 3:
                    raise KeyboardInterrupt
            except KeyboardInterrupt:
                sys.exit(1)

    def exit(self):
        if not self.finished and not self.silent_exit:
            sys.exit(1)


class StoppingSignal(Exception):
    def __init__(self, *args, silent=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.silent = silent
