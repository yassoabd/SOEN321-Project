from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    # Render the front-end HTML file
    return render_template('index.html')

@app.route('/hello', methods=['POST'])
def hello():
    # Respond with a JSON message
    return jsonify(message="Hello World")

if __name__ == '__main__':
    app.run(debug=True)
