# ASGI app with full request handling

async def app(scope, receive, send):
    path = scope.get('path', '/')
    method = scope.get('method', 'GET')
    
    headers = [(b'content-type', b'application/json')]
    
    # GET requests
    if method == 'GET':
        if path == '/' or path == '':
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [(b'content-type', b'text/html')],
            })
            await send({
                'type': 'http.response.body',
                'body': b'<html><body><h1>EduForge API</h1></body></html>',
            })
        elif path == '/api/lessons':
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': headers,
            })
            await send({
                'type': 'http.response.body',
                'body': b'{"lessons": [], "total": 0}',
            })
        else:
            await send({
                'type': 'http.response.start',
                'status': 404,
                'headers': headers,
            })
            await send({
                'type': 'http.response.body',
                'body': b'{"error": "not found"}',
            })
        return
    
    # POST requests - read body
    if method == 'POST':
        # Read body from receive
        body = b''
        while True:
            event = await receive()
            if event.get('type') == 'http.request':
                body = event.get('body', b'')
                break
        
        # Parse body
        import json
        data = {}
        try:
            if body:
                data = json.loads(body)
        except:
            pass
        
        # Route POST requests
        if path == '/api/generate-content':
            title = data.get('title', 'Generated Lesson')
            response = {
                'id': '1',
                'title': title,
                'category': data.get('category', 'standard'),
                'standard': {'intro': 'intro', 'body': 'body', 'questions': [], 'activities': []},
                'simplified': {'intro': 's', 'body': 's', 'questions': [], 'activities': []},
                'accessibility': {'intro': 'a', 'body': 'a', 'questions': [], 'activities': []},
                'ui_hints': {},
                'version': 1
            }
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': headers,
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps(response).encode(),
            })
        
        elif path == '/api/analyze-content':
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': headers,
            })
            await send({
                'type': 'http.response.body',
                'body': b'{"score": 75, "readability": 70}',
            })
        
        elif path == '/api/suggest-improvements':
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': headers,
            })
            await send({
                'type': 'http.response.body',
                'body': b'{"suggestions": []}',
            })
        
        elif path == '/api/curriculum/generate':
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': headers,
            })
            await send({
                'type': 'http.response.body',
                'body': b'{"course_id": "1", "course_title": "Course"}',
            })
        
        elif path == '/api/live-assist':
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': headers,
            })
            await send({
                'type': 'http.response.body',
                'body': b'{"suggestions": []}',
            })
        
        elif path == '/api/smart-analyze':
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': headers,
            })
            await send({
                'type': 'http.response.body',
                'body': b'{"score": 75}',
            })
        
        else:
            await send({
                'type': 'http.response.start',
                'status': 404,
                'headers': headers,
            })
            await send({
                'type': 'http.response.body',
                'body': b'{"error": "not found"}',
            })
        return
    
    # Default
    await send({
        'type': 'http.response.start',
        'status': 405,
        'headers': headers,
    })
    await send({
        'type': 'http.response.body',
        'body': b'{"error": "method not allowed"}',
    })