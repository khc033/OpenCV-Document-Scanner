from flask import Flask, flash, request, url_for, redirect, jsonify, render_template
import urllib.request
from werkzeug.utils import secure_filename
from scan import DocScanner

import json
import os
import argparse

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPG'])
UPLOAD_FOLDER = os.path.join('static', 'output')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response


# @app.route("/")
# def upload_form():
#     return render_template('upload.html')

@app.route('/', methods=['POST'])
def get_path(file_path):

	if allowed_file(file_path):
		filename = secure_filename(file_path)
		scanner = DocScanner()
		#print('upload_image filename: ' + filename)
		print('Image successfully uploaded and displayed below')
		return scanner.scan(filename)
	else:
		print('Allowed image types are -> png, jpg, jpeg, gif')



@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='outpu0t/' + filename), code=301)

if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  group = ap.add_mutually_exclusive_group(required=True)
  group.add_argument("--images", help="Directory of images to be scanned")
  group.add_argument("--image", help="Path to single image to be scanned")
  ap.add_argument("-i", action='store_true',
      help = "Flag for manually verifying and/or setting document corners")

  args = vars(ap.parse_args())
  im_dir = args["images"]
  im_file_path = args["image"]
  interactive_mode = args["i"]
  
  scanner = DocScanner(interactive_mode)

  valid_formats = [".jpg", ".jpeg", ".jp2", ".png", ".bmp", ".tiff", ".tif"]

  get_ext = lambda f: os.path.splitext(f)[1].lower()

  # Scan single image specified by command line argument --image <IMAGE_PATH>
  if im_file_path:
      scanner.scan(im_file_path)

  # Scan all valid images in directory specified by command line argument --images <IMAGE_DIR>
  else:
      im_files = [f for f in os.listdir(im_dir) if get_ext(f) in valid_formats]
      for im in im_files:
          scanner.scan(im_dir + '/' + im)
  # app.run(debug=True, host='0.0.0.0', port=5000)