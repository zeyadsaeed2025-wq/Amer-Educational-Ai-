from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test-post', methods=['POST'])
def test_post():
    return jsonify({'success': True, 'method': 'POST'})

@app.route('/test-get')
def test_get():
    return jsonify({'success': True, 'method': 'GET'})

@app.route('/')
def index():
    return 'EduForge API Works!'

# Must be named 'app'
app = app