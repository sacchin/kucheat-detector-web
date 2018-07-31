#!/usr/bin/python
# -*- coding: utf-8 -*-

# [Import start]
from flask import Blueprint, render_template
# [Import end]

app = Blueprint('detector_api', __name__, static_url_path='/static', static_folder='./static')
# , url_prefix='/hoge')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect')
def detect():
    return "\ncoming soon"
