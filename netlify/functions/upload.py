"""
Netlify Function for file upload
Adapted from Flask route for serverless deployment
"""
import json
import os
import base64
import tempfile
from PIL import Image
from pillow_heif import register_heif_opener
from pdf2image import convert_from_bytes

register_heif_opener()

def handler(event, context):
    """Handle file upload request"""
    try:
        # Parse request
        if event.get('httpMethod') != 'POST':
            return {
                'statusCode': 405,
                'body': json.dumps({"error": "Method not allowed"})
            }
        
        # Parse body (Netlify functions receive base64 encoded body)
        body = event.get('body', '')
        if event.get('isBase64Encoded'):
            body = base64.b64decode(body)
        
        # For multipart form data, we need to parse it
        # Note: Netlify has limitations with file uploads
        # Consider using Netlify Forms or external storage (S3) for production
        
        # For now, return a simplified response
        # In production, you'd want to use Netlify Forms or direct S3 upload
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "error": "File upload via Netlify Functions has limitations. Consider using Netlify Forms or direct S3 upload for production.",
                "note": "For PoC, use a platform like Render or Railway that supports file uploads better."
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }

