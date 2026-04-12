from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/test', methods=['POST'])
def test():
    # Try different ways to get data
    data = request.get_json(silent=True) or {}
    form = request.form or {}
    return jsonify({
        'success': True,
        'json_data': data,
        'form_data': dict(form),
        'content_type': request.content_type
    })

app = app