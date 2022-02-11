import curses


class Base:
    def paint(self, screen, application):
        pass


class CursorComponent(Base):
    def __init__(self, config):
        super().__init__()
        self.cursor_position = None

    def update(self, screen):
        self.cursor_position = screen.getyx()

    def paint(self, screen, application):
        if self.cursor_position:
            screen.move(*self.cursor_position)


class TextComponent(Base):
    def paint_text(self, screen, text, color):
        screen.addstr(text, curses.color_pair(color))


class StatsComponent(TextComponent):
    def __init__(self, config):
        super().__init__()
        self.color = config.get("stats_color")
        self.template = config.get("stats_template")

    def init(self, screen, application):
        super().init(screen, application)

    def paint(self, screen, application):
        usedy, _ = screen.getyx()
        maxy, _ = screen.getmaxyx()

        text = self.template.format(stats=application.stats)

        texty = len(text.splitlines())

        if texty + usedy + 1 < maxy:
            self.paint_text(screen, text, self.color)


class TopMargin(Base):
    def __init__(self, config):
        super().__init__()
        self.height = config.get("top_margin_percentage") / 100

    def paint(self, screen, application):
        maxy, _ = screen.getmaxyx()
        lines = int(self.height * maxy)
        for line in range(lines):
            screen.addstr("\n")


class TextBox(TextComponent):
    """
    Wraps lines of text elements writing to it nicely
    """

    def __init__(self, config, cursor_component):
        super().__init__()
        self.cursor_component = cursor_component

        self.maxy, self.maxx = None, None
        self.usedy, self.usedx = None, None

        self.left_margin = config.get("left_margin_percentage")

        self.valid_color = config.get("user_input_valid_color")
        self.invalid_color = config.get("user_input_invalid_color")
        self.color = config.get("reference_text_color")

        self.lines_on_screen = config.get("lines_on_screen")

    def clear(self):
        self.maxy, self.maxx = None, None
        self.usedy, self.usedx = None, None

    @property
    def max_line_x(self):
        return int(self.maxx * (100 - self.left_margin - self.left_margin) / 100) - 1

    @property
    def padding(self):
        return " " * int(1 + self.left_margin * self.maxx / 100)

    def lines_to_display(self, application):
        text = application.get_text()
        valid_position = application.valid_user_text_position()
        user_position = application.user_position()

        lines = []
        line = ""
        word = ""

        valid_pointer = (0, 0)
        user_pointer = (0, 0)

        for i, c in enumerate(text):
            word += c

            if len(line + word) > self.max_line_x:
                lines.append(line)
                line = ""

            if not c.isalnum():
                word = str(word)[:-1] + " "
                line += word
                word = ""

        if word:
            line += word

        if line:
            lines.append(line)

        position = 0
        for i, l in enumerate(lines):
            st, end = position, position + len(l)
            if user_position >= st and user_position <= end:
                user_pointer = (i, user_position - st)
            if valid_position >= st and valid_position <= end:
                valid_pointer = (i, valid_position - st)
            position = end

        return lines, valid_pointer, user_pointer

    def paint_line(self, i, line, valid_pointer, user_pointer, screen):
        if i < valid_pointer[0]:
            # easy, we are in written line
            self.paint_text(screen, line, self.valid_color)
            self.cursor_component.update(screen)
            return

        if i > user_pointer[0]:
            # easy, we are in reference line
            self.paint_text(screen, line, self.color)
            return

        valid_text = ""
        invalid_text = ""
        invalid_start = 0

        if i == valid_pointer[0]:
            valid_text = line[: valid_pointer[1]]
            invalid_start = valid_pointer[1]
            invalid_text = line[valid_pointer[1] :]
        if i == user_pointer[0]:
            invalid_text = line[invalid_start : user_pointer[1]]

        reference_text = line[len(invalid_text) + len(valid_text) :]
        invalid_text = invalid_text.replace(" ", "_")

        self.paint_text(screen, valid_text, self.valid_color)
        self.paint_text(screen, invalid_text, self.invalid_color)
        self.cursor_component.update(screen)
        self.paint_text(screen, reference_text, self.color)

    def paint(self, screen, application):
        self.maxy, self.maxx = screen.getmaxyx()
        self.usedy, self.usedx = screen.getyx()

        lines, valid_pointer, user_pointer = self.lines_to_display(application)

        lines_fitting = min((self.maxy - self.usedy, self.lines_on_screen))
        start = 0
        end = len(lines)

        if lines_fitting == 0:
            raise Exception("Too small display!")

        if lines_fitting <= len(lines):
            previous_lines = 1 if lines_fitting > 2 else 0
            next_lines = 1 if lines_fitting > 1 else 0
            start = user_pointer[0] - previous_lines
            end = user_pointer[0] + next_lines
            if start == -1:
                end += 1

        for i, line in enumerate(lines):
            if i >= start and i <= end:
                screen.addstr(self.padding)
                self.paint_line(i, line, valid_pointer, user_pointer, screen)
                screen.addstr("\n")

        self.clear()
