from .infrastructure.pipelines import *

dummy_pipeline = RecoDummyPipeline(features=["text_emb"])
dummy_text_pipeline = TextFaissPipeline(prompt="Dance")
