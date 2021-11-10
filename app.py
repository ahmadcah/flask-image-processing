# web-app for API image manipulation
from flask import Flask, request, render_template, send_from_directory
import os
import cv2
from werkzeug.utils import redirect
import process as process

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# default access page
@app.route("/")
def main():
    return render_template('proses.html')


# upload selected image and forward to processing page
@app.route("/proses1", methods=['POST'])
def proses1():
    target = os.path.join(APP_ROOT, 'static/images/')
    filename = request.files['file']
    print('filename : ', filename)

    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    # save file
    data = os.path.join(target, "query.jpg")
    filename.save(data)
    # img = cv2.imread(data, cv2.IMREAD_GRAYSCALE)
    img = data
    print(img)
    # check mode
    if 'otsu' in request.form.get('select_thresholding'):
        mode = 'otsu'
    elif 'niblack' in request.form.get('select_thresholding'):
        mode = 'niblack'
    elif 'sauvola' in request.form.get('select_thresholding'):
        mode = 'sauvola'
    elif 'medianBlur15' in request.form.get('select_thresholding'):
        mode = 'medianBlur15'
    elif 'morphology7x7' in request.form.get('select_thresholding'):
        mode = 'morphology7x7'
    elif 'gradientOrientation' in request.form.get('select_thresholding'):
        mode = 'gradientOrientation'
    elif 'cannyWide' in request.form.get('select_thresholding'):
        mode = 'cannyWide'

    # process
    if mode == 'otsu':
        print('start otsu')
        img_res = process.otsu_thresh(img)
        print(img_res)
        cv2.imwrite("/".join([target, 'result.jpg']), img_res)
    elif mode == 'niblack':
        img_res = process.niblack_thresh(img)
        cv2.imwrite("/".join([target, 'result.jpg']), img_res)
    elif mode == 'sauvola':
        img_res = process.sauvola_thresh(img)
        cv2.imwrite("/".join([target, 'result.jpg']), img_res)
    elif mode == 'medianBlur15':
        img_res = process.medianBlur15(img)
        cv2.imwrite("/".join([target, 'result.jpg']), img_res)
    elif mode == 'morphology7x7':
        img_res = process.morphology7x7(img)
        cv2.imwrite("/".join([target, 'result.jpg']), img_res)
    elif mode == 'gradientOrientation':
        img_res = process.gradientOrientation(img)
        cv2.imwrite("/".join([target, 'result.jpg']), img_res)
    elif mode == 'cannyWide':
        img_res = process.cannyWide(img)
        cv2.imwrite("/".join([target, 'result.jpg']), img_res)

    # forward to processing page
    return redirect('/')


# retrieve file from 'static/images' directory
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)


if __name__ == "__main__":
    app.run(debug=True)
