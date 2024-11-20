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

@app.route('/todos', methods=['POST'])
def add_todo():

    data = request.json
    todo_id = mongo.db.todos.insert_one(data).inserted_id
    new_todo = mongo.db.todos.find_one({"_id": todo_id})
    
    return jsonify({"id": str(new_todo["_id"]), "text": new_todo["text"]}), 201

@app.route('/todos', methods=['GET'])
def get_todos():

    todos = mongo.db.todos.find()
    result = [{"id": str(todo["_id"]), "text": todo["text"]} for todo in todos]

    return jsonify(result), 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("FILE UPLOAD RECEIVED")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
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
