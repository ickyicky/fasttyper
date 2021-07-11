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


class TextBox(TextComponent):
    """
    Wraps lines of text elements writing to it nicely
    """

    class Element:
        def __init__(self, text, color, triggers_cursor=False):
            self.text = text
            self.color = color
            self.triggers_cursor = triggers_cursor
            self.next = None

    def __init__(self, config, cursor_component):
        super().__init__()
        self.cursor_component = cursor_component

        self.elements = []

        self.maxy, self.maxx = None, None
        self.usedy, self.usedx = None, None

    def clear(self):
        self.elements = []

        self.maxy, self.maxx = None, None
        self.usedy, self.usedx = None, None

    def add_element(self, text, color, triggers_cursor=False):
        element = self.Element(text, color, triggers_cursor)

        if self.elements:
            self.elements[-1].next = element

        self.elements.append(element)

    def find_first_word(self, element):
        if element is None:
            return ""

        if len(element.text) == 0:
            return self.find_first_word(element.next)

        if not element.text[0].isalnum():
            return ""

        return element.text.split()[0] + " "

    @property
    def max_line_x(self):
        return self.maxx - 1

    def prepare_text_element(self, element):
        lines = []
        line = ""
        word = ""
        next_word = self.find_first_word(element.next)

        for char in element.text + next_word:
            if char.isalnum():
                word += char
            elif char == "\n" or len(word) + len(line) + self.usedx >= self.max_line_x:
                lines.append(line)
                word += " "
                line = ""
                line += word
                word = ""
                self.usedx = 0
                if self.usedy >= self.maxy:
                    break
            else:
                word += char
                line += word
                word = ""

        if len(word) > 0:
            if len(word) + len(line) + self.usedx >= self.max_line_x:
                lines.append(line)
                line = word
            else:
                line += word

        if len(line) > 0:
            lines.append(line)

        if len(lines) == 0 or (len(lines) == 1 and lines[0] == next_word):
            return ""

        if next_word:
            last_line = lines[-1]
            if len(last_line) == 0:
                lines = lines[:-1]
            lines[-1] = lines[-1][: -len(next_word)]

        lines = lines[: self.maxy - self.usedy]
        return "\n".join(lines)

    def pain_element(self, screen, element):
        self.usedy, self.usedx = screen.getyx()
        self.maxy, self.maxx = screen.getmaxyx()
        text = self.prepare_text_element(element)
        self.paint_text(screen, text, element.color)

        if element.triggers_cursor:
            self.cursor_component.update(screen)

    def paint(self, screen, application):

        for element in self.elements:
            self.pain_element(screen, element)

        self.clear()


class UserInput(Base):
    def __init__(self, config, text_box):
        super().__init__()
        self.text_box = text_box
        self.valid_color = config.get("user_input_valid_color")
        self.invalid_color = config.get("user_input_invalid_color")

    def paint(self, screen, application):
        valid_text, invalid_text = application.get_user_text()

        invalid_text = invalid_text.replace(" ", "_")

        self.text_box.add_element(valid_text, self.valid_color)
        self.text_box.add_element(invalid_text, self.invalid_color, True)


class ReferenceText(Base):
    def __init__(self, config, text_box):
        super().__init__()
        self.text_box = text_box
        self.color = config.get("reference_text_color")

    def paint(self, screen, application):
        valid_user_text_position = application.valid_user_text_position()
        reference_text = application.get_reference_text(valid_user_text_position)
        self.text_box.add_element(reference_text, self.color)
