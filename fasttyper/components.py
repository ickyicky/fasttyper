import curses


class Base:
    def __init__(self):
        self.rows = None
        self.cols = None

    def init(self, screen, application):
        self.rows, self.cols = screen.getmaxyx()

    def paint(self, screen, application):
        pass


class CursorComponent(Base):
    def __init__(self):
        super().__init__()
        self.cursor_position = None

    def update(self, screen):
        self.cursor_position = screen.getyx()

    def paint(self, screen, application):
        screen.move(*self.cursor_position)


class UserInput(Base):
    def __init__(self, cursor_component):
        super().__init__()
        self.cursor_component = cursor_component
        self.valid_color = None
        self.invalid_color = None

    def init(self, screen, application):
        super().init(screen, application)
        self.valid_color = application.config.get("user_input_valid_color")
        self.invalid_color = application.config.get("user_input_invalid_color")

    def paint(self, screen, application):
        valid_text, invalid_text = application.get_user_text()

        invalid_text = invalid_text.replace(" ", "_")
        invalid_text = invalid_text.replace("\n", "\\n")

        screen.addstr(valid_text, curses.color_pair(self.valid_color))
        screen.addstr(invalid_text, curses.color_pair(self.invalid_color))
        self.cursor_component.update(screen)


class ReferenceText(Base):
    def __init__(self):
        super().__init__()
        self.color = None

    def init(self, screen, application):
        super().init(screen, application)
        self.color = application.config.get("reference_text_color")

    def paint(self, screen, application):
        valid_user_text_position = application.valid_user_text_position()
        reference_text = application.get_reference_text(valid_user_text_position)
        reference_text = reference_text.replace("\n", "\\n\n")
        screen.addstr(reference_text, curses.color_pair(self.color))


class StatsComponent(Base):
    def __init__(self):
        super().__init__()
        self.color = None
        self.template = None

    def init(self, screen, application):
        super().init(screen, application)
        self.color = application.config.get("stats_color")
        self.template = application.config.get("stats_template")

    def paint(self, screen, application):
        screen.addstr(
            self.template.format(stats=application.stats), curses.color_pair(self.color)
        )
