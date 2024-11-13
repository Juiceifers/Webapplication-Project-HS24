# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/api/hello')
def hello():
    return jsonify(message="Hello from Flask!")


app.run(debug=True)
app.run(host='172.23.66.241', port=52091, debug=True)


if __name__ == '__main__':
    app.run(debug=True)




# http://172.23.66.241/