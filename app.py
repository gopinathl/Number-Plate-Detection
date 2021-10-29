# coding=utf-8
import sys
sys.path.append(r'/home/dell/Desktop/Number Plate Detection')
import os
from flask import Flask, request, url_for, redirect, render_template
from src.resources.upload_image import UploadImageResource
from src.resources.get_results import GetResultsResource


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r'/home/dell/Desktop/Number Plate Detection/Data_Folder/car images'
app.config['OUTPUT_FOLDER'] = r'static/output'
app.config["BUNDLE_ERRORS"] = True
app.config['DEFAULT_PARSERS'] = [
    'flask.ext.api.parsers.JSONParser',
    'flask.ext.api.parsers.URLEncodedParser',

    'flask.ext.api.parsers.MultiPartParser'
]

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        upload_obj = UploadImageResource()
        upload_status, filename = upload_obj.post()
        if upload_status == 'success':
            get_results_obj = GetResultsResource()
            license_plate_text, result_img = get_results_obj.get()

            return redirect(url_for('result', lp=license_plate_text, img1=result_img[0], img2=result_img[1]))

    return render_template('home.html')

@app.route('/result <lp> <img1> <img2>', methods=['GET', 'POST'])
def result(lp, img1, img2):
    if request.method == 'POST':
        get_results_obj = GetResultsResource()
        get_results_obj.post()
        return redirect(url_for('upload_file'))
    img1 = os.path.join(app.config['OUTPUT_FOLDER'], img1)
    img2 = os.path.join(app.config['OUTPUT_FOLDER'], img2)

    return render_template('result.html', lp_text=lp, image1=img1, image2=img2)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)