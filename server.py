from flask import Flask, request, jsonify, flash, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from flask import Flask
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

app = Flask(__name__)

from Mert_testing import summarizer
from topic_mods.main import process_file

#CORS(app, origins="http://localhost:8080", supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
CORS(app)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/tododb"
#mongo = PyMongo(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("FILE UPLOAD RECEIVED")
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            fpath = f"uploads/{filename}"

            process_file(fpath)
            summarizer.summarize_pdf(fpath)

            #return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
# Additional routes for update and delete can be added similarly

if __name__ == '__main__':
    print("starting flask API")
    app.run(host='0.0.0.0', port=5000)
