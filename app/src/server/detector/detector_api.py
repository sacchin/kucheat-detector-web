#!/usr/bin/python
# -*- coding: utf-8 -*-

# [Import start]
import os
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug import secure_filename
# [Import end]

app = Blueprint('detector_api', __name__, static_folder='static')
# , url_prefix='/hoge')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        img_file = request.files['img_file']
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            print(filename, os.path.join('./uploads', filename))

            img_file.save(os.path.join('./uploads', filename))
            img_url = '/uploads/' + filename

            return jsonify(ResultSet={"result": img_url})
        else:
            return jsonify(ResultSet={"result": "ext is not allowed"})

    return jsonify(ResultSet={"result": "only support post"})

