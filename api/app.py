from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    return jsonify({
        'path': path,
        'method': request.method
    })

if __name__ == '__main__':
    app.run(debug=True)