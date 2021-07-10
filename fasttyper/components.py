import curses


class Base:
    def __init__(self):
        self.rows = None
        self.cols = None

    def init(self, screen):
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

    def paint(self, screen, application):
        valid_text, invalid_text = application.get_user_text()

        invalid_text = invalid_text.replace(" ", "_")
        invalid_text = invalid_text.replace("\n", "\\n")

        screen.addstr(valid_text, curses.color_pair(3))
        screen.addstr(invalid_text, curses.color_pair(2))
        self.cursor_component.update(screen)


class ReferenceText(Base):
    def paint(self, screen, application):
        valid_user_text_position = application.valid_user_text_position()
        reference_text = application.get_reference_text(valid_user_text_position)
        reference_text = reference_text.replace("\n", "\\n\n")
        screen.addstr(reference_text, curses.color_pair(8))


class StatsComponent(Base):
    def paint(self, screen, application):
        text = f"\n\nwpm: {application.stats.correct_words / application.stats.total_minutes}"
        text += f"\ntime: {application.stats.total_seconds}s"
        screen.addstr(text, curses.color_pair(5))
