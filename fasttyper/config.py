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
        "wpm_graph_color": 3,
        "raw_wpm_graph_color": 9,
        "errors_graph_color": 2,
    }

    def __init__(self, configmap):
        self.configmap = configmap

    def get(self, key):
        return self.configmap.get(key, self.defaults[key])
