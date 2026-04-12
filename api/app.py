from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    method = request.method
    
    # GET requests
    if method == 'GET':
        if path in ['api/lessons', 'health']:
            return jsonify({'status': 'ok', 'path': path})
        return '', 404
    
    # POST requests - just return success
    if method == 'POST':
        # Get body
        data = request.get_json(silent=True) or {}
        if not data:
            data = {'received': 'ok'}
        
        return jsonify({
            'status': 'success',
            'received': data,
            'path': path
        })
    
    return jsonify({'error': 'method not allowed'}), 405