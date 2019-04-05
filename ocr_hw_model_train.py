#!/usr/bin/env python
from __future__ import division, unicode_literals
from app.base.base_model import BaseModel
from .src.model.utils.data_generator import DataGenerator
from .src.model.utils.general import Config
from .src.model.utils.text import Vocab, load_formulas
from .src.model.utils.image import greyscale, build_images
from .src.model.img2seq_ctc import Img2SeqCtcModel
from .src.model.evaluation.text import score_files
from .src.model.evaluation.image import score_dirs
from .src.model.utils.image import greyscale


class OcrCtcModel(BaseModel):
    def __init__(self):
        pass

    def load_models(self, data_path, vocab_path, model_path, model_weight, dir_output):
        config_data = Config(data_path)
        config_vocab = Config(vocab_path)
        config_model = Config(model_path)

        vocab = Vocab(config_vocab)
        self.model = Img2SeqCtcModel(config_model, dir_output, vocab)
        self.model.build_pred()
        self.model.restore_session(model_weight)

    def predict(self, img):
        img = greyscale(img)
        res = self.model.predict(img)

        return res, None
