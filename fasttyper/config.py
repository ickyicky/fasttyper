class Config:
    defaults = {
        "user_input_valid_color": 3,
        "user_input_invalid_color": 2,
        "reference_text_color": 8,
        "stats_template": "\n\nwpm: {stats.wpm}\ntime: {stats.total_seconds}s",
        "stats_color": 5,
        "summary_template": (
            "WPM: {stats.wpm}\n"
            "CPM: {stats.cpm}\n"
            "RAW WPM: {stats.raw_wpm}\n"
            "RAW CPM: {stats.raw_cpm}\n"
            "total seconds: {stats.total_seconds}\n"
            "total minutes: {stats.total_minutes}\n"
            "correct words: {stats.correct_words}\n"
            "correct chars: {stats.correct_chars}\n"
            "incorrect words: {stats.incorrect_words}\n"
            "incorrect chars: {stats.incorrect_chars}\n"
            "total words: {stats.total_words}\n"
            "total chars: {stats.total_chars}\n"
            "accuracy: {stats.accuracy}%"
        ),
        "summary_datafile": "~/.cache/fasttyper/datafile.csv",
    }

    def __init__(self, configmap):
        self.configmap = configmap

    def get(self, key):
        return self.configmap.get(key, self.defaults[key])
