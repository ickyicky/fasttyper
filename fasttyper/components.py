import curses


class WindowComponent:
    """
    Basic text component printing inside window
    """

    def __init__(self, config):
        self._window = None
        self._height = None
        self._width = None
        self._begin_x = None
        self._begin_y = None

        self.cursor_x, self.cursor_y = 0, 0

    def update_size(self, height, width, begin_x, begin_y):
        self._height = height
        self._width = width
        self._begin_x = begin_x
        self._begin_y = begin_y

    def init_window(self):
        self._window = curses.newwin(
            self._height,
            self._width,
            self._begin_y,
            self._begin_x,
        )

    def set_box(self, i):
        self._window.box(i, i)

    def paint_text(self, row, col, text, color):
        self._window.addstr(row, col, text, curses.color_pair(color))

    def move(self, x, y):
        self._window.move(x, y)

    def paint(self, screen, application):
        pass

    def refresh(self):
        self._window.refresh()


class BorderedBox(WindowComponent):
    """
    Adds border to WindowComponent
    """

    def __init__(self, config):
        super().__init__(config)

        self.maxy, self.maxx = None, None

        self.pos_y = config.get("top_margin_percentage") / 100
        self.pos_x = config.get("left_margin_percentage") / 100
        self.height = config.get("lines_on_screen")
        self.width = None

    def paint_text(self, row, col, text, color):
        super().paint_text(row + 1, col + 1, text, color)

    def move(self, x, y):
        super().move(x + 1, y + 1)

    def init(self, screen, application):
        self.width = int(self.maxx * (1 - 2 * self.pos_x))
        self.update_size(
            self.height + 2,
            self.width + 2,
            int(self.pos_x * self.maxx) - 1,
            int(self.pos_y * self.maxy) - 1,
        )
        self.init_window()
        self.set_box(1)

        screen.refresh()


class BufferDependentComponent(BorderedBox):
    """
    Adds content source from buffer
    """

    def __init__(self, config):
        super().__init__(config)

        self.buffered_lines = 0
        self.buffer = None
        self.last_hidden_word = 0
        self.lines = [[] for _ in range(self.height)]

        from .buffer import CharType

        self.chtype_mapper = {
            CharType.valid: config.get("user_input_valid_color"),
            CharType.invalid: config.get("user_input_invalid_color"),
            CharType.reference: config.get("reference_text_color"),
        }

        self.current_word_idx = 0
        self.current_line, self.word_index = 0, 0

    def set_buffer(self, buffer):
        self.buffer = buffer

    def line_len(self, index):
        spaces = max(len(self.lines[index]) - 1, 0)
        return sum([len(w) for w in self.lines[index]]) + spaces

    def paint_line(self, line_nr):
        pos = 0

        for i, word in enumerate(self.lines[line_nr]):
            for c in word:
                self.paint_text(line_nr, pos, c[0], self.chtype_mapper[c[1]])
                pos += 1

            if i != len(self.lines[line_nr]):
                self.paint_text(line_nr, pos, " ", 0)
                pos += 1

    def fill_lines(self):
        line_nr = self.buffered_lines
        start_idx = self.last_hidden_word + sum(
            [len(line) for line in self.lines[:line_nr]]
        )

        for i in range(start_idx, self.buffer.total_words):
            word = self.buffer.get_word(i)

            if self.line_len(line_nr) + len(word) + 1 > self.width:
                self.paint_line(line_nr)
                line_nr += 1

                if line_nr >= self.height:
                    break

            self.lines[line_nr].append(word)

        self.paint_line(line_nr)
        self.buffered_lines = self.height

    def update_cursor(self):
        self.cursor_x = self.current_line
        past_words = self.lines[self.current_line][: self.word_index]
        self.cursor_y = (
            sum([len(w) for w in past_words])
            + len(past_words)
            + self.buffer.current_char
        )

    def update_current_word(self, word_index):
        """
        This is called by buffer. It signals that user changed its state.

        First, active word is updated. It changes on added char or deleted word.
        """

        old_len = len(self.lines[self.current_line][self.word_index])
        self.lines[self.current_line][self.word_index] = self.buffer.get_word(
            self.current_word_idx
        )
        new_len = len(self.lines[self.current_line][self.word_index])

        if old_len != new_len:
            pass

        while word_index > self.current_word_idx:
            self.word_index += 1

            if self.word_index >= len(self.lines[self.current_line]):
                self.word_index = 0
                self.current_line += 1

            self.current_word_idx += 1
            self.lines[self.current_line][self.word_index] = self.buffer.get_word(
                self.current_word_idx
            )

        while word_index < self.current_word_idx:
            self.word_index -= 1

            if self.word_index == -1:
                self.current_line -= 1
                self.word_index = len(self.lines[self.current_line] - 1)

            self.current_word_idx -= 1
            self.lines[self.current_line][self.word_index] = self.buffer.get_word(
                self.current_word_idx
            )

        self.update_cursor()


class BorderWithImprintedStats(BufferDependentComponent):
    """
    Imprints stats on one of borders
    """

    def __init__(self, config):
        super().__init__(config)

        self.stats_template = config.get("stats_template").replace("\n", " ")
        self.stats_color = config.get("stats_color")
        self.stats_row = -1 if config.get("stats_position") == "top" else self.height

    def paint_stats(self):
        text = self.stats_template.format(stats=self.buffer.stats)
        if len(text) < self.width - 2:
            self.paint_text(self.stats_row, 2, text, self.stats_color)


class TextBox(BorderWithImprintedStats):
    """
    Calls all inherited paint functions and inits windows
    """

    def __init__(self, config):
        super().__init__(config)

    def paint(self, screen, application):
        if self._window is None:
            self.maxy, self.maxx = screen.getmaxyx()
            self.init(screen, application)

        if self.buffered_lines < self.height:
            self.fill_lines()

        self.paint_stats()
        self.paint_line(self.current_line)
        self.move(self.cursor_x, self.cursor_y)
        self.refresh()
