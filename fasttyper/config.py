class Config:
    defaults = {
        "user_input_valid_color": 3,
        "user_input_invalid_color": 2,
        "reference_text_color": 9,
        "stats_template": "wpm: {stats.wpm:0.2f}, time: {stats.total_seconds:0.2f}s",
        "stats_color": 5,
        "stats_position": "top",
        "summary_datafile": "~/.cache/fasttyper/datafile.csv",
        "top_margin_percentage": 40,
        "left_margin_percentage": 35,
        "min_width": 80,
        "lines_on_screen": 3,
        "border": 1,
        "logo": " ~ FastTyper ~ ",
        "logo_color": 8,
        "resume_text": " press <Tab> to continue, <Ctrl>C to exit ",
        "resume_text_color": 9,
        "summary_template": (
            "wpm: {wpm:5.1f}   |   peak: {peak_wpm:5.1f}",
            "raw: {raw_wpm:5.1f}   |   peak: {peak_raw_wpm:5.1f}",
            "acc: {accuracy:5.1f}%  |   words: {correct_words}/{total_words}",
            "time: {total_seconds:5.1f}s ",
        ),
        "summary_centered": True,
        "summary_color": 9,
        "summary_lines": 4,
        "summary_border": 0,
        "random_capitalization": 0,
        "random_punctuation": 0,
        "sentence_mode": False,
        "punctuation": ",.?!;:",
        "sentence_ending": ".?!",
        "amount": 25,
        "language": "english",
        "no_cursor": False,
        "unclutter_backspace": False,
    }

    def __init__(self, configmap):
        self.configmap = configmap

    def get(self, key):
        return self.configmap.get(key, self.defaults[key])
