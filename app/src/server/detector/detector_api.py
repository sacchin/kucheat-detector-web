#!/usr/bin/python
# -*- coding: utf-8 -*-

# [Import start]
import os
import numpy as np
import pickle
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug import secure_filename
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from keras.preprocessing import image
from imageio import imread
from scipy.misc import imresize
from keras.applications.imagenet_utils import preprocess_input
from server.detector.ssd import SSD300
from server.detector.ssd_utils import BBoxUtility
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
    save_path = current_app.config['SAVE_PATH']

    if request.method == 'POST':
        img_file = request.files['userfile']
        saved, filename = saveImage(save_path, img_file)

        if saved:
            uploadGoogleDrive(save_path, filename)
            return jsonify(ResultSet={"result": filename})
        else:
            return jsonify(ResultSet={"result": "ext is not allowed"})

    return jsonify(ResultSet={"result": "only support post"})


def saveImage(save_path, img_file):
    if img_file and allowed_file(img_file.filename):
        filename = secure_filename(img_file.filename)
        dir_preparation(save_path)
        img_file.save(os.path.join(save_path, filename))
        return (True, filename)

    return (False, "image file is null or file name isn't correct")


def uploadGoogleDrive(save_path, filename):
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
    f.SetContentFile(os.path.join(save_path, filename))
    f.Upload()

def ssd_predict(save_path, filename):
    weight_file = current_app.config['WEIGHT_FILE']
    mawile_pkl_file = current_app.config['MAWILE_PICKLE_FILE']
    prior_pkl_file = current_app.config['PRIOR_PICKLE_FILE']
    input_shape = (300, 300, 3)
    NUM_CLASSES = 21

    model = SSD300(input_shape, num_classes=NUM_CLASSES)
    model.load_weights(weight_file, by_name=True)

    priors = pickle.load(open(prior_pkl_file, 'rb'))
    bbox_util = BBoxUtility(NUM_CLASSES, priors)

    img = image.load_img(os.path.join(save_path, filename), target_size=(300, 300))
    img = image.img_to_array(img)
    inputs = preprocess_input(np.array([img.copy()]))
    preds = model.predict(inputs, batch_size=1, verbose=1)
    results = bbox_util.detection_out(preds)

    det_label = results[0][:, 0]
    det_conf = results[0][:, 1]
    det_xmin = results[0][:, 2]
    det_ymin = results[0][:, 3]
    det_xmax = results[0][:, 4]
    det_ymax = results[0][:, 5]

    # Get detections with confidence higher than 0.6.
    top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.6]

    top_conf = det_conf[top_indices]
    top_label_indices = det_label[top_indices].tolist()
    top_xmin = det_xmin[top_indices]
    top_ymin = det_ymin[top_indices]
    top_xmax = det_xmax[top_indices]
    top_ymax = det_ymax[top_indices]

    box_array = []
    for i in range(top_conf.shape[0]):
        xmin = int(round(top_xmin[i] * img.shape[1]))
        ymin = int(round(top_ymin[i] * img.shape[0]))
        xmax = int(round(top_xmax[i] * img.shape[1]))
        ymax = int(round(top_ymax[i] * img.shape[0]))
        label = int(top_label_indices[i])
        display_txt = '{:0.2f}, {}'.format(top_conf[i], label)
        box_array.append({'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax, 'label': label, 'display_txt': display_txt})

    return box_array
