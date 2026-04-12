from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/lessons':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'lessons': [], 'total': 0}).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0) or 0)
            body = self.rfile.read(length) if length > 0 else b''
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        if self.path == '/api/generate-content':
            title = data.get('title', 'test')
            resp = json.dumps({
                'id': '1', 'title': title, 'category': 'standard',
                'standard': {'intro': 'intro', 'body': 'body', 'questions': [], 'activities': []},
                'simplified': {'intro': 'intro', 'body': 'body', 'questions': [], 'activities': []},
                'accessibility': {'intro': 'intro', 'body': 'body', 'questions': [], 'activities': []},
                'ui_hints': {}, 'version': 1
            })
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(resp.encode())
        else:
            self.send_response(404)
            self.end_headers()

app = handler