#-*-coding:utf-8 -*-

import os
from multiprocessing import Manager
from configparser import ConfigParser

__manager = None
config = None

MAX_STATE_CNT = 300


def init_global_config():
    global config
    if config is None:
        config = __manager.dict()
    return config


class Configs:

    def __init__(self, env="production"):
        filename = "settings/" + env + ".conf"
        config_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), filename)
        self.config = ConfigParser()
        self.config.read(config_path)


    def __getitem__(self, section, item):
        return self.config.get(section, item)

    get = __getitem__
