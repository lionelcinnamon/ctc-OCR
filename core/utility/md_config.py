#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from shutil import copyfile
from .md_path import MdPath


class MdConfig(MdPath):
    """
        Class that loads hyperparameters from json file into attributes
    """

    def __init__(self, source, model_root=None, config_root=None, data_root=None):
        super(MdConfig, self).__init__(model_root, config_root, data_root)
        """
        Args:
            source: path to json file or dict
        """
        self.source = source

        if type(source) is dict:
            self.__dict__.update(source)
        elif type(source) is list:
            for s in source:
                self.load_json(s)
        else:
            self.load_json(source)

    def load_json(self, source):
        if self.root_dir is not None:
            source = self.get_config_path(source)

        with open(source) as f:
            data = json.load(f)
            self.__dict__.update(data)

    def save(self, dir_name):
        # self.ensure_dir(dir_name)
        if type(self.source) is list:
            for s in self.source:
                c = MdConfig(s)
                c.save(dir_name)
        elif type(self.source) is dict:
            json.dumps(self.source, indent=4)
        else:
            source = self.get_root_path(self.source)
            copyfile(source, self.get_file_path(dir_name, self.export_name))

    def get(self, variable_name, default=None):
        if variable_name is not None:
            variable_names = variable_name.split('.')
            result = self.__dict__
            for var_name in variable_names:
                if isinstance(result, dict):
                    result = result.get(var_name)

            return result

    def get_path(self, variable_name, v_type='R'):
        """
        :param variable_name:
        :param v_type:
                'O': original,
                'R': root path,
                'C': config path,
                'M': model path,
                'D': data path
        :return:
        """
        val = self.get(variable_name)
        val = self.get_full_path(val, v_type)

        return val

    @property
    def dict_json(self):
        print(json.dumps(self.__dict__, indent=4))

    @staticmethod
    def show_json(json_data):
        print(json.dumps(json_data, indent=4))
