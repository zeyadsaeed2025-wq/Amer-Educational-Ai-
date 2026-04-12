# Vercel Python Serverless Function
# Format: handler(request, context) -> dict

def handler(request, context):
    """Vercel serverless function handler."""
    path = request.path
    method = request.method
    
    # Route based on path and method
    if path == '/api/lessons' and method == 'GET':
        return {
            'statusCode': 200,
            'body': '{"lessons": [], "total": 0}',
            'headers': {'Content-Type': 'application/json'}
        }
    
    if path == '/api/generate-content' and method == 'POST':
        return {
            'statusCode': 200,
            'body': '{"id": "1", "title": "Generated", "category": "standard"}',
            'headers': {'Content-Type': 'application/json'}
        }
    
    if path == '/api/analyze-content' and method == 'POST':
        return {
            'statusCode': 200,
            'body': '{"score": 75, "readability": 70}',
            'headers': {'Content-Type': 'application/json'}
        }
    
    # Default - frontend
    return {
        'statusCode': 200,
        'body': '<html><body>EduForge API</body></html>',
        'headers': {'Content-Type': 'text/html'}
    }