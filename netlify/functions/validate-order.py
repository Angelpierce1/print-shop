"""
Netlify Function for order validation
"""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from agent import PrintShopAgent
except ImportError:
    PrintShopAgent = None

def handler(event, context):
    """Handle order validation"""
    try:
        if event.get('httpMethod') != 'POST':
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": "Method not allowed"})
            }
        
        body = event.get('body', '{}')
        if event.get('isBase64Encoded'):
            import base64
            body = base64.b64decode(body).decode('utf-8')
        
        data = json.loads(body)
        
        if not PrintShopAgent:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    "valid": False,
                    "error": "Agent not available in Netlify Functions"
                })
            }
        
        agent = PrintShopAgent()
        
        # Note: File validation requires file storage
        # Netlify Functions have /tmp but it's ephemeral
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "valid": False,
                "error": "File validation requires persistent storage. Netlify Functions have limitations for file uploads.",
                "recommendation": "Use Render, Railway, or Heroku for full file upload support."
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": str(e)})
        }

