# Vercel Python - Always return 200

def handler(request, context):
    """Always return 200 with JSON."""
    return {
        'statusCode': 200,
        'body': '{"success": true}',
        'headers': {'Content-Type': 'application/json'}
    }