import curses


class Interface:
    def __init__(self, application, components):
        self.application = application
        self.components = components

    def init_colors(self):
        assert curses.has_colors()
        curses.start_color()
        curses.use_default_colors()

        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

    def init(self, screen):
        self.init_colors()

    def update(self, screen):
        screen.clear()
        for component in self.components:
            component.paint(screen, self.application)
        screen.refresh()

    def __call__(self, screen):
        """
        Main running loop
        """
        self.init(screen)
        self.application.start()

        while self.application.running():
            self.update(screen)
            self.application.action(screen)
