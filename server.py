from flask import Flask, request, jsonify, flash, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from flask import Flask
from werkzeug.utils import secure_filename
import database  # Import your database functions
import os
from flask_cors import CORS

app = Flask(__name__)

from Mert_testing import summarizer
from topic_mods.main import process_file

#CORS(app, origins="http://localhost:8080", supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
#app.config["MONGO_URI"] = "mongodb://localhost:27017/tododb"
#mongo = PyMongo(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)
database.create_table()  # Ensure the table is created



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

            print("valid file")

            print(request.form, len(request.form))
            print("Files len:", len(request.files))

            user_name = request.json["user_name"]
            map_name = request.form["map_name"]

            print(user_name, map_name)

            filename = secure_filename(file.filename)

            database.add_map(map_name, user_name, filename)

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


# Initialize the SQLite database
database.create_table()  # Ensure the table is created

# Routes for registration and login
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    # Check if the user already exists in the database
    if database.get_user(username):
        return jsonify({"success": False, "message": "User already exists"})

    # Add user to the database
    database.add_user(username, password)
    return jsonify({"success": True, "message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    print("login main", username)

    # Fetch user from the database
    user = database.get_user(username)
    if user and user[2] == password:  # Compare stored password (user[2]) with the entered password
        return jsonify({"success": True, "username": username})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})


if __name__ == '__main__':
    print("starting flask API")
    app.run(host='0.0.0.0', port=5000)
