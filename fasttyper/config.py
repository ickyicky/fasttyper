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
        "lines_on_screen": 3,
        "logo": "~FastTyper~",
        "logo_color": 8,
        "resume_text": "press any key to continue, <Ctrl>C to exit",
        "resume_text_color": 9,
        "end_template": (
            "wpm: {wpm:.1f}/{peak_wpm:.1f}  raw: {raw_wpm:.1f}/{peak_raw_wpm:.1f}",
            "acc: {accuracy:.1f}  chars: {correct_chars}/{total_chars}  words: {correct_words}/{total_words}",
            "time: {total_seconds:.1f}s",
        ),
        "end_color": 9,
    }

    def __init__(self, configmap):
        self.configmap = configmap

    def get(self, key):
        return self.configmap.get(key, self.defaults[key])
