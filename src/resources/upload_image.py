# coding=utf-8
import os
import urllib.request
from flask import Flask, flash, request, redirect, jsonify, render_template, make_response, url_for
from flask_restful import Resource, Api, reqparse
import werkzeug
from werkzeug.utils import secure_filename


class UploadImageResource:
    def __init__(self):
        self.UPLOAD_FOLDER = r'/home/dell/Desktop/Number Plate Detection/Data_Folder/car images'

    def allowed_file(self, filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def post(self):
        # check if the post request has the file part

        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # filename=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(os.path.join(self.UPLOAD_FOLDER, filename))
                status = 'success'
                return status, filename
