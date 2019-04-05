#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import cv2
from core.utility.md_config import MdConfig

from core.model.img2seq_ctc import Img2SeqCtcModel
from core.model.utils.image import greyscale

module_path = os.path.dirname(__file__)
sys.path.append(module_path)


class KVExtract(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    model_path = os.path.join(os.path.dirname(__file__), 'models')
    config = MdConfig(['configs/model.json', 'configs/vocab.json', 'configs/log.json'])
    model = Img2SeqCtcModel(config)
    model.build_pred()
    model.restore_session()
    img_paths = ['data/imgs/18.3.26.png', 'data/imgs/18.10.12.png']
    for img_path in img_paths:
        img = greyscale(cv2.imread(img_path))
        res = model.predict(img)
        print(res)
