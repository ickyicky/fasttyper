import curses


class Interface:
    def __init__(self, application, components, end_components, no_cursor=False):
        self.application = application
        self.components = components
        self.end_components = end_components
        self.no_cursor = no_cursor
        self.colors = True

    def init_colors(self):
        try:
            assert curses.has_colors()
        except AssertionError:
            self.colors = False
            return

        curses.start_color()
        curses.use_default_colors()

        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

    def init(self, screen):
        screen.clear()
        self.init_colors()

    def update(self, screen):
        for component in self.components:
            component.paint(screen, self.application)

    def draw_end(self, screen):
        for component in self.end_components:
            component.paint(screen, self.application)

    def __call__(self, screen):
        """
        Main running loop
        """
        self.init(screen)
        self.application.start()

        if self.no_cursor:
            curses.curs_set(0)

        while self.application.running():
            self.update(screen)
            self.application.action(screen)

        if self.application.summarize():
            screen.clear()
            curses.curs_set(0)
            self.draw_end(screen)
            self.application.action(screen)
