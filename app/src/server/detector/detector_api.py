#!/usr/bin/python
# -*- coding: utf-8 -*-

# [Import start]
import os
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug import secure_filename
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
# [Import end]

app = Blueprint('detector_api', __name__, static_folder='static')
# , url_prefix='/hoge')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def dir_preparation(upload_path):
    if os.path.exists(upload_path):
        logger = current_app.logger
        logger.info("upload folder exists")
    else:
        os.makedirs(upload_path)


@app.route('/index')
def index():
    logger = current_app.logger
    logger.info("serving index")
    return render_template('index.html')


@app.route('/detect', methods=['GET', 'POST'])
def detect():
    upload_path = current_app.config['UPLOAD_PATH']

    if request.method == 'POST':
        img_file = request.files['userfile']
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            dir_preparation(upload_path)
            img_file.save(os.path.join(upload_path, filename))
            img_url = '/uploads/' + filename

            a(filename)

            return jsonify(ResultSet={"result": img_url})
        else:
            return jsonify(ResultSet={"result": "ext is not allowed"})

    return jsonify(ResultSet={"result": "only support post"})


def a(filename):
    upload_path = current_app.config['UPLOAD_PATH']
    folder_id = current_app.config['DRIVE_FOLDER_ID']

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    f = drive.CreateFile({
        'title':
        filename,
        'mimeType':
        'image/jpeg',
        'parents': [{
            'kind': 'drive#fileLink',
            'id': folder_id
        }]
    })
    f.SetContentFile(os.path.join(upload_path, filename))
    f.Upload()
