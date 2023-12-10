FEATURE_LIST = [
    "text_emb",
    "activity",
    "dress_code",
    "place",
]


class RecoDummyPipeline:
    def __init__(self, features: list):
        for f in features:
            if f not in FEATURE_LIST:
                print("features should be in one of: ", FEATURE_LIST)
                return
        self.features = features

    def predict_list(self, prompt: str, image: str):
        out_filters = {}
        for f in self.features:
            # DO MAGIC
            out_filters[f] = 0

        return out_filters


class TextDummyPipeline:
    def __init__(self, prompt: str):
        # LOAD DATA AND FITTING
        self.prompt = prompt

    def predict_list(self):
        # DO MAGIC
        return [1, 2, 3, 4]
