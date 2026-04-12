from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test():
    return jsonify({'success': True})

app = app