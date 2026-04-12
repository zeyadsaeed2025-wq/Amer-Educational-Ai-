from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'EduForge API'})

@app.route('/api/test', methods=['POST'])
def test():
    return jsonify({'success': True})

app = app