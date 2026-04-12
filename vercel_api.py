import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import FastAPI app
from main import app as fastapi_app

# Vercel Python handler
def handler(request, context):
    """Handle incoming requests."""
    from starlette.requests import Request
    from starlette.responses import Response
    import asyncio
    
    # Create ASGI scope from Vercel request
    scope = {
        'type': 'http',
        'method': request.method,
        'path': request.path,
        'query_string': request.query.encode('utf-8'),
        'headers': [(k.lower(), v) for k, v in request.headers.items()],
        'server': (request.hostname, 80),
    }
    
    async def receive():
        body = request.body or b''
        return {'type': 'http.request', 'body': body}
    
    async def send(message):
        pass  # Response handled by Vercel
    
    # Run the app
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            fastapi_app(scope, receive, send)
        )
        loop.close()
        return response
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": str(e)}