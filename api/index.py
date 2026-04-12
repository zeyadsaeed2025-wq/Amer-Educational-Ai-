def handler(request, context):
    """Handle all requests - including OPTIONS for CORS"""
    method = request.method
    
    # Handle OPTIONS (CORS preflight)
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'body': '',
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
    
    # All other methods - return success
    return {
        'statusCode': 200,
        'body': '{"success": true, "method": "' + method + '"}',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }