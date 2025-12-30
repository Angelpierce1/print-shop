"""
Netlify Function for order submission with AI guardrails
"""
import json
import os
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from agent import PrintShopAgent
except ImportError:
    # Fallback if imports fail
    PrintShopAgent = None

def handler(event, context):
    """Handle order submission"""
    try:
        if event.get('httpMethod') != 'POST':
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": "Method not allowed"})
            }
        
        # Parse JSON body
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
                    "error": "Agent not available",
                    "note": "Netlify Functions have limitations. Consider Render or Railway for full functionality."
                })
            }
        
        agent = PrintShopAgent()
        
        # Prepare order data
        filename = data.get('filename', '')
        # Note: File paths won't work in serverless - need S3 or similar
        file_path = f"/tmp/{filename}"  # Temporary path (won't exist)
        
        order_data = {
            'email': data.get('email', ''),
            'name': data.get('name', ''),
            'size': data.get('size', ''),
            'paper': data.get('paper', '100lb Matte'),
            'quantity': data.get('quantity', 1),
            'file_path': file_path,
            'filename': filename
        }
        
        # Process order
        result = agent.process_order(order_data)
        
        if not result['valid']:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    "success": False,
                    "error": result.get('error', result.get('message', 'Order validation failed')),
                    "layer": result.get('layer', 'unknown'),
                    "message": result.get('message', 'Please fix the errors and try again.')
                })
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "success": True,
                "message": "Order validated and submitted successfully!",
                "order_summary": result.get('order_summary', {}),
                "note": "Netlify Functions have file storage limitations. For production, use Render or Railway."
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": str(e)})
        }

