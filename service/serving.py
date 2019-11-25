# -*-coding:utf-8 -*-

from flask import Blueprint

serving_module = Blueprint('serving', __name__, url_prefix='/serving')


@serving_module.route('/api/test')
def check():
    return 'The service is ok', 200
