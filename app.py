# Vercel ASGI app
# Uses ASGI instead of WSGI/Flask

async def app(scope, receive, send):
    """ASGI application."""
    path = scope.get('path', '/')
    method = scope.get('method', 'GET')
    
    # Headers
    headers = [(b'content-type', b'application/json')]
    
    if path == '/':
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [(b'content-type', b'text/html')],
        })
        await send({
            'type': 'http.response.body',
            'body': b'<html><body><h1>EduForge API Works!</h1></body></html>',
        })
    
    elif path == '/test-post' and method == 'POST':
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': headers,
        })
        await send({
            'type': 'http.response.body',
            'body': b'{"success": true}',
        })
    
    elif path == '/api/lessons':
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': headers,
        })
        await send({
            'type': 'http.response.body',
            'body': b'{"lessons": []}',
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