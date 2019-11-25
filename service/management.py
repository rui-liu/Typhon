# -*-coding:utf-8 -*-

from flask import Blueprint

management_module = Blueprint('management', __name__, url_prefix='/management')
