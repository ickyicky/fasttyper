import curses
from .application import StoppingSignal


class Interface:
    def __init__(self, application, components, summary_components, no_cursor=False):
        self.application = application
        self.components = components
        self.summary_components = summary_components
        self.no_cursor = no_cursor
        self.colors = True
        self.max_color = None

        for component in self.components:
            component.set_interface(self)

        for component in self.summary_components:
            component.set_interface(self)

    def init_colors(self):
        try:
            assert curses.has_colors()
        except AssertionError:
            self.colors = False
            return

        curses.start_color()
        curses.use_default_colors()

        for i in range(0, curses.COLORS):
            self.max_color = i + 1
            try:
                curses.init_pair(i + 1, i, -1)
            except Exception:
                break

    def init(self, screen):
        screen.clear()
        self.init_colors()

    def update(self, screen):
        for component in self.components:
            component.paint(screen, self.application)

    def draw_summary(self, screen):
        for component in self.summary_components:
            component.paint(screen, self.application)

    def normalize_color(self, color):
        if not self.colors:
            0

        return color % self.max_color

    def __call__(self, screen):
        """
        Main running loop
        """
        self.init(screen)
        self.application.start()

        if self.no_cursor:
            curses.curs_set(0)
        else:
            curses.curs_set(1)

        while self.application.running():
            self.update(screen)
            self.application.action(screen)

        if self.application.summarize():
            screen.clear()
            curses.curs_set(0)
            self.draw_summary(screen)

            while self.application.action(screen):
                pass
