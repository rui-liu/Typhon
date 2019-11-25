# -*-coding:utf-8 -*-
import json


class ModelConfig:

    @classmethod
    def parse_config(cls, path):
        with open(path, 'r') as fp:
            conf = json.load(fp)
            config = ModelConfig(conf['id'], conf['name'])
            config.epoch = conf['epoch']
            #模型类型，暂时打算支持binary, multi-class, regression
            config.model_type = conf['model_type']
            config.features = ModelConfig.parse_features(conf['features'])

    @classmethod
    def parse_features(cls, f):
        return 1

    def __init__(self, model_id, model_name):
        self.id = model_id
        self.name = model_name
