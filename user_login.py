from flask import Flask, request, jsonify
import database  # Import the database functions

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    print("USER:", username)

    # Fetch user from the database
    user = database.get_user(username)  # Using the imported function
    if user and user[2] == password:  # Compare stored password (user[2]) with the entered password
        # Successful login
        return jsonify({"success": True, "username": username})
    else:
        # Invalid login
        return jsonify({"success": False, "message": "Invalid username or password"})

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    # Check if the user already exists in the database
    if database.get_user(username):  # Using the imported function
        return jsonify({"success": False, "message": "User already exists"})
    
    # Add user to the database
    database.add_user(username, password)  # Using the imported function
    return jsonify({"success": True, "message": "User registered successfully"})

if __name__ == '__main__':
    app.run(debug=True)
