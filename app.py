from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import cv2
import pytesseract
import numpy as np
import AksharaJaana.main as ak
from googletrans import Translator
import shutil


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
translator = Translator()

print('translator initialise')
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

port = int(os.environ.get('PORT'))

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        
        result=''

        lines = ak.ocr_engine(file_path)
        n=4000
        res = [lines[i:i+n] for i in range(0, len(lines), n)]
        detlang = translator.detect(lines[0:1000]).lang
        for i in range(len(res)):
            if detlang != 'en':
                res[i]=translator.translate(res[i], dest='en')
            result+= str(res[i])
 
        shutil.rmtree(os.path.join(basepath,'output'))
        os.remove(file_path)
        return result
    return None

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        print(2)
        # Get the file from post request
        f = request.files['file']
        print(3)
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        print(4)
        result=''
        img = cv2.imread(file_path)
        print(7)
        #lines = str(pytesseract.image_to_string(img,lang='kan')) #ak.ocr_engine(file_path)
        lines = ak.ocr_engine(file_path)
        n=4000
        print(5)
        res = [lines[i:i+n] for i in range(0, len(lines), n)]
        detlang = translator.detect(lines[0:1000]).lang
        print(6)
        for i in range(len(res)):
            if detlang != 'en':
                res[i]=translator.translate(res[i], dest='en')
            result+= str(res[i])
        print(7)
        shutil.rmtree(os.path.join(basepath,'output'))
        os.remove(file_path)
        print(8)
        return result
    return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

