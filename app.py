from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

# Serve static files from current directory
@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

@app.route('/')
def index():
    return send_from_directory('.', 'frontend.html')

# Alias to app for Vercel
app = app
handler = app