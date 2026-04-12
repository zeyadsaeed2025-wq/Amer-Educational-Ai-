from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/test')
def test():
    return jsonify({'test': 'ok'})

@app.route('/api/anything', methods=['POST'])
def anything():
    return jsonify({'ok': True})