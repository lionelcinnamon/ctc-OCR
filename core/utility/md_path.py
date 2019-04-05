#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Prints the tree structure for the path specified on the command line
    Make structure folder of module
"""
import os


class MdPath(dict):
    def __init__(self, model_root=None, config_root=None, data_root=None):

        """
        :param model_root: path of model dict
        :param config_root: path of config dict
        :param data_root: path od data dict
        """
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if model_root is not None:
            self.model_root = model_root
        else:
            self.model_root = self.root_dir

        if config_root is not None:
            self.config_root = config_root
        else:
            self.config_root = self.root_dir

        if data_root is not None:
            self.data_root = data_root
        else:
            self.data_root = self.root_dir

    @staticmethod
    def ensure_dir(directory):
        """
        Make dir if it not exist
        :param directory:
        :return:
        """
        if directory is not None:
            if not os.path.exists(directory):
                os.makedirs(directory)

    @staticmethod
    def get_file_path(root_dir, file_path):
        file_path = os.path.join(root_dir, file_path)
        return file_path

    def make_structure(self, source):
        if type(source) is str:
            self.ensure_dir(source)
        elif type(source) is list:
            for s in source:
                self.ensure_dir(s)

    def get_full_path(self, i_path, i_type='R'):
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
        if i_path is not None:
            # if isinstance(i_path, str):
            if i_type.upper() == 'R':
                i_path = self.get_root_path(i_path)
            elif i_type.upper() == 'C':
                i_path = self.get_config_path(i_path)
            elif i_type.upper() == 'M':
                i_path = self.get_model_path(i_path)
            elif i_type.upper() == 'D':
                i_path = self.get_data_path(i_path)
            # elif isinstance(i_path, list):
            #     for idx, i_p in enumerate(i_path):
            #         i_path[idx] = self.get_full_path(i_p, i_type)

            return i_path

    def get_root_path(self, file_path):
        file_path = self.get_file_path(self.root_dir, file_path)
        self.ensure_dir(os.path.dirname(file_path))
        return file_path

    def get_model_path(self, file_path):
        file_path = self.get_file_path(self.model_root, file_path)
        self.ensure_dir(os.path.dirname(file_path))
        return file_path

    def get_config_path(self, file_path):
        file_path = self.get_file_path(self.config_root, file_path)
        self.ensure_dir(os.path.dirname(file_path))
        return file_path

    def get_data_path(self, file_path):
        file_path = self.get_file_path(self.data_root, file_path)
        self.ensure_dir(os.path.dirname(file_path))
        return file_path


if __name__ == '__main__':
    md_path = MdPath()
    dir_ = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'configs')
    input_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs')
    print(md_path.get_model_path(input_dir))
