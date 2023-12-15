FEATURE_LIST = [
    "text_emb",
    "activity",
    "dress_code",
    "place",
]


class RecoDummyPipline:
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


class TextDummyPipline:
    def __init__(self):
        # LOAD DATA AND FITTING
        pass

    def sample_mapper(self, sample):
        id = 0
        return id

    def predict_list(self, prompt: str):
        # DO MAGIC
        # predict
        # map

        return [1, 2, 3, 4]
