from flask import Flask, render_template
from . import detector
import os
import logging
from logging.handlers import RotatingFileHandler


def not_exist_makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def init_app(app):
    log_path = app.config['LOG_PATH']

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )
    debug_log = os.path.join(log_path, 'debug.log')
    not_exist_makedirs(os.path.dirname(debug_log))

    debug_file_handler = RotatingFileHandler(
        debug_log, maxBytes=100000, backupCount=10
    )

    debug_file_handler.setLevel(logging.INFO)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(log_path, 'error.log')
    not_exist_makedirs(os.path.dirname(error_log))
    error_file_handler = RotatingFileHandler(
        error_log, maxBytes=100000, backupCount=10
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

    app.logger.setLevel(logging.DEBUG)


app = Flask(__name__, instance_relative_config=True)
app.config['JSON_AS_ASCII'] = False
app.config.from_object('config.default')
init_app(app)

blueprints = [detector]
for blueprint in blueprints:
    app.register_blueprint(blueprint.app)