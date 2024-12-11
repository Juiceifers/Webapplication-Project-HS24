from flask import Flask, request, jsonify, flash, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from flask import Flask, render_template
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

        print("FILES:", request.files)

        #if 'file' not in request.files:
        #    flash('No file part')
        #    return redirect(request.url)
        
        user_name = request.form.get("user_name")
        map_name = request.form.get("map_name")


        root = os.path.dirname(os.path.abspath(__file__))
        map_path = os.path.join(root, "user_data", user_name, map_name)

        #files = request.files['file']
        files = request.files.getlist('files') 
        filepaths = []

        print(request.form, len(request.form))
        print("Files len:", len(request.files))
        print(f"Request content type: {request.content_type}")



        for file in files:

            #if file.filename == '':
            #    flash('No selected file')
            #    return redirect(request.url)

            if file and allowed_file(file.filename):

                print("valid file")

                print(user_name, map_name)

                filename = secure_filename(file.filename)

                #if not os.path.exists(map_path):


                os.makedirs(map_path, exist_ok=True)

                print(os.path.join(map_path, filename))

                file.save(os.path.join(map_path, filename))

                fpath = f"{map_path}/{filename}"

                print("FILE PATH:", fpath)
                
                filepaths.append(fpath)


        database.add_map(map_name, user_name, filepaths)
        render_text = process_file(filepaths)

        map_file_path = os.path.join(map_path, f"MAP_{map_name}.html")
        
        with open(map_file_path, "w", encoding="utf-8") as txt_map_file:
            txt_map_file.write(render_text)


        user = database.get_user(user_name)
        if user:
            maps = database.get_user_maps(user[0])
        else:
            maps = []

        return render_text

        #return jsonify({
        #                "success": True,
        #                "message": "Files uploaded and processed successfully",
        #                "map_name": map_name,
        #                "render_text": render_text,
        #                "filenames": filepaths,
        #                "maps": [
        #                    {
        #                        "id": map_item[0],
        #                        "user_id": map_item[1],
        #                        "map_name": map_item[2],
        #                        "files": map_item[3]
        #                    } for map_item in maps
        #                ] if maps else []
        #            }), 200
        #

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


# Initialize the SQLite database
database.create_table() 


@app.route('/', methods=['GET'])
def mainpage():
    return render_template("index.html")

@app.route('/login.html', methods=['GET'])
def loginpage():
    return render_template("login.html")

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

    user_path = f"/user_data/{username}" 
    if not os.path.exists(user_path):
        os.makedirs(user_path)


    return jsonify({"success": True, "message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    print("login main", username)

    # Fetch user from the database
    user = database.get_user(username)
    if user and user[2] == password:  # Compare stored password (user[2]) with the entered password

        # Retrieve user's maps
        maps = database.get_user_maps(user[0])
        
        # Convert maps to a list of dictionaries for JSON serialization
        maps_list = []
        if maps:
            maps_list = [
                {
                    "id": map_item[0],
                    "user_id": map_item[1],
                    "map_name": map_item[2],
                    "files": map_item[3]
                } for map_item in maps
            ]
        
        # Successful login
        return jsonify({
            "success": True,
            "username": username,
            "maps": maps_list
        })
    else:
        # Invalid login
        return jsonify({"success": False, "message": "Invalid username or password"})




if __name__ == '__main__':
    print("starting flask API")
    #app.run(host='0.0.0.0', port=52091)
    app.run(host='0.0.0.0', port=5000)

    #http://172.23.66.241:52091