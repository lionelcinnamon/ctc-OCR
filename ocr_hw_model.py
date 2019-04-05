#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
from app.base.base_model import BaseModel
from .core.utility.md_config import MdConfig
from .core.model.img2seq_ctc import Img2SeqCtcModel
from .core.model.utils.image import greyscale


class OcrCtcModel(BaseModel):
    def __init__(self):
        super(BaseModel, self).__init__()
        pass

    def load_models(self, config_path, vocab_path, model_root):
        config_vocab = MdConfig(vocab_path, model_root)
        config_model = MdConfig(config_path, model_root)

        self.model = Img2SeqCtcModel(config_model, config_vocab)
        self.model.build_pred()
        self.model.restore_session()

    def predict(self, img):
        res = ['']
        try:
            img = greyscale(img)
            res = self.model.predict(img)
        except:
            self.afw_logging.exception()

        return res, [0]
