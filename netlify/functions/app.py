import os
import sys
import json
from werkzeug.serving import WSGIRequestHandler

# Add parent directories to path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

# Import Flask app
from main import app

def handler(event, context):
    """
    Netlify Functions handler for Flask app
    """
    try:
        # Get request details
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query_params = event.get('queryStringParameters') or {}
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        # Build query string
        query_string = ''
        if query_params:
            query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
        
        # Create WSGI environ
        environ = {
            'REQUEST_METHOD': http_method,
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)) if body else '0',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': body.encode() if isinstance(body, str) else body,
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False
        }
        
        # Add headers to environ
        for key, value in headers.items():
            key = 'HTTP_' + key.upper().replace('-', '_')
            environ[key] = value
        
        # Response data
        response_data = []
        status = None
        response_headers = []
        
        def start_response(status_code, headers_list):
            nonlocal status, response_headers
            status = status_code
            response_headers = headers_list
        
        # Call Flask app
        app_response = app(environ, start_response)
        
        # Collect response
        for data in app_response:
            response_data.append(data)
        
        # Build response
        body_content = b''.join(response_data).decode('utf-8')
        status_code = int(status.split()[0])
        
        # Convert headers
        headers_dict = {}
        for header_name, header_value in response_headers:
            headers_dict[header_name] = header_value
        
        return {
            'statusCode': status_code,
            'headers': headers_dict,
            'body': body_content
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in Netlify function: {error_details}")
        
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': str(e),
                'details': error_details
            })
        }
