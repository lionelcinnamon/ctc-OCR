#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from core.utility.md_config import MdConfig
from core.utility.md_utils import tree

module_path = os.path.dirname(__file__)
sys.path.append(module_path)


class KVExtract(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    model_path = os.path.join(os.path.dirname(__file__), 'models')
    tree('core')
    config = MdConfig('configs/model.json')
    # vocab = MdConfig('configs/vocab.json', model_path)
    config.dict_json
    print('attn_cell_config.cell_type:', config.get('attn_cell_config.cell_type'))
    print('attn_cell_config.num_units:', config.get('attn_cell_config.num_units'))
    print(config.get_path('model_path', 'R'))
    print(config.get_path('model_path', 'C'))
    print(config.get_path('model_path', 'M'))
    print(config.get_path('model_path', 'D'))
    print(config.get_path('model_path1', 'D'))

    config.show_json(config.attn_cell_config.get('cell_type'))
