from flask import Flask, flash, request, url_for, redirect, jsonify, render_template
import urllib.request
from service import ToDoService
from models import Schema
from werkzeug.utils import secure_filename

import json
import os

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


@app.route("/")
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='output/' + filename), code=301)

# @app.route("/test", methods=['GET', 'POST'])
# def get_picture():
#     return render_template('hello.html')

# @app.route("/picture_view")
# def picture_view():
#     filename = os.path.join(app.config['UPLOAD_FOLDER'], 'sample_1.jpg')
#     return render_template('picture-view.html', upload_img = filename)


# @app.route("/<name>")
# def hello_name(name):
#     return "Hello " + name


# @app.route("/todo", methods=["GET"])
# def list_todo():
#     return jsonify(ToDoService().list())


# @app.route("/todo", methods=["POST"])
# def create_todo():
#     return jsonify(ToDoService().create(request.get_json()))


# @app.route("/todo/<item_id>", methods=["PUT"])
# def update_item(item_id):
#     return jsonify(ToDoService().update(item_id, request.get_json()))

# @app.route("/todo/<item_id>", methods=["GET"])
# def get_item(item_id):
#     return jsonify(ToDoService().get_by_id(item_id))

# @app.route("/todo/<item_id>", methods=["DELETE"])
# def delete_item(item_id):
#     return jsonify(ToDoService().delete(item_id))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)