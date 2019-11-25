# -*-coding:utf-8 -*-

import os
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import json
import logging
from logging.handlers import TimedRotatingFileHandler
from service.serving import serving_module
from service.management import management_module
from service.training import training_module
from service.model import model_module

log_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), "log")
if not os.path.exists(log_path):
    os.mkdir(log_path)

app = Flask(__name__)
log = None


@app.route('/check_backend_active.html')
def dummy_service():
    return 'hello world', 200


def parse_args():
    import argparse as ap
    from sys import argv
    parser = ap.ArgumentParser(description="Arguments to start the server.")
    parser.add_argument("--mode", nargs='?', default='test', required=False, choices=['debug', 'test', 'production'],
                        help='deploy model of the server, either test or production')
    return parser.parse_args(argv[1:])


def register_modules():
    app.register_blueprint(serving_module)
    app.register_blueprint(model_module)
    app.register_blueprint(training_module)
    app.register_blueprint(management_module)


if __name__ == '__main__':
    args = parse_args()
    import globals

    config = globals.Configs(env=args.mode)
    globals.config = config

    log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
    formatter = logging.Formatter(log_fmt)
    # 创建TimedRotatingFileHandler对象
    log_file_handler = TimedRotatingFileHandler(filename="log/application.log", when="D", interval=1, backupCount=10)
    log_level = globals.config.get("application", "LOG_LEVEL")
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=log_level)
    log = logging.getLogger()
    log.addHandler(log_file_handler)

    register_modules()

    server = WSGIServer(
        ('0.0.0.0', int(globals.config.get("application", "PORT"))), app)
    # server.start()
    server.serve_forever()
