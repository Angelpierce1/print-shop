"""Simple test endpoint to verify Vercel Python functions work."""

import json

def handler(req):
    """Simple test handler."""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "success": True,
            "message": "Vercel Python function is working!",
            "path": getattr(req, "path", "unknown"),
            "method": getattr(req, "method", "unknown")
        })
    }


