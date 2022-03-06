class Config:
    defaults = {
        "user_input_valid_color": 3,
        "user_input_invalid_color": 2,
        "reference_text_color": 8,
        "stats_template": "wpm: {stats.wpm:0.2f}, time: {stats.total_seconds:0.2f}s",
        "stats_color": 5,
        "stats_position": "top",
        "summary_template": (
            "WPM: {stats.wpm:0.2f}\n"
            "CPM: {stats.cpm:0.2f}\n"
            "RAW WPM: {stats.raw_wpm:0.2f}\n"
            "RAW CPM: {stats.raw_cpm:0.2f}\n"
            "total seconds: {stats.total_seconds:0.2f}\n"
            "total minutes: {stats.total_minutes:0.2f}\n"
            "correct words: {stats.correct_words}\n"
            "correct chars: {stats.correct_chars}\n"
            "incorrect words: {stats.incorrect_words}\n"
            "incorrect chars: {stats.incorrect_chars}\n"
            "total words: {stats.total_words}\n"
            "total chars: {stats.total_chars}\n"
            "accuracy: {stats.accuracy:0.2f}%"
        ),
        "summary_datafile": "~/.cache/fasttyper/datafile.csv",
        "top_margin_percentage": 40,
        "left_margin_percentage": 35,
        "lines_on_screen": 3,
    }

    def __init__(self, configmap):
        self.configmap = configmap

    def get(self, key):
        return self.configmap.get(key, self.defaults[key])
