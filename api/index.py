"""Flask app for Print Shop AI Order Guardrail - Vercel serverless function."""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from flask import Flask, request, jsonify
from PIL import Image
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass  # pillow-heif is optional
try:
    from pdf2image import convert_from_bytes
except ImportError:
    convert_from_bytes = None

# Import agent - adjust path as needed
try:
    from agent import PrintShopAgent
    agent = PrintShopAgent()
except ImportError:
    agent = None

# Initialize Flask app - MUST be named 'app' for Vercel
app = Flask(__name__)

# For Vercel serverless, use /tmp for uploads
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MIN_DPI = 225

def send_approval_email(email, filename, status):
    """Simulates sending an email"""
    print(f"--- EMAIL SENT TO {email} ---")
    print(f"Subject: Order Update - {status}")
    print(f"Body: Your design '{filename}' is {status}.")
    print("-------------------------------")
    return True

@app.route('/')
def index():
    """Root endpoint - returns API info."""
    return jsonify({
        "success": True,
        "message": "Print Shop AI Order Guardrail API",
        "endpoints": {
            "upload": "/upload",
            "submit_order": "/submit-order",
            "validate_order": "/validate-order"
        }
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload file endpoint."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = file.filename.lower()
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    
    try:
        if filename.endswith('.pdf'):
            if convert_from_bytes is None:
                return jsonify({"error": "PDF conversion not available"}), 500
            file_data = file.read()
            images = convert_from_bytes(file_data)
            img = images[0]
            new_filename = filename.replace('.pdf', '.jpg')
            filepath = os.path.join(UPLOAD_FOLDER, new_filename)
            img.save(filepath, 'JPEG')
        elif filename.endswith('.heic'):
            img = Image.open(file)
            new_filename = filename.replace('.heic', '.jpg')
            filepath = os.path.join(UPLOAD_FOLDER, new_filename)
            img.save(filepath, "JPEG")
        else:
            file.save(filepath)
            img = Image.open(filepath)

        width_px, height_px = img.size
        
        return jsonify({
            "success": True,
            "filename": os.path.basename(filepath),
            "width": width_px,
            "height": height_px,
            "message": "File uploaded successfully"
        })
    except Exception as e:
        return jsonify({"error": f"File processing error: {str(e)}"}), 500

@app.route('/submit-order', methods=['POST'])
def submit_order():
    """Submit order with AI Order Guardrail validation."""
    if not agent:
        return jsonify({"error": "Agent not available"}), 500
    
    data = request.json or {}
    
    filename = data.get('filename', '')
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        base_name = os.path.splitext(filename)[0]
        for ext in ['.jpg', '.jpeg', '.png', '.pdf']:
            test_path = os.path.join(UPLOAD_FOLDER, base_name + ext)
            if os.path.exists(test_path):
                file_path = test_path
                filename = os.path.basename(test_path)
                break
    
    order_data = {
        'email': data.get('email', ''),
        'name': data.get('name', ''),
        'size': data.get('size', ''),
        'paper': data.get('paper', '100lb Matte'),
        'quantity': data.get('quantity', 1),
        'file_path': file_path,
        'filename': filename
    }
    
    result = agent.process_order(order_data)
    
    if not result.get('valid', False):
        return jsonify({
            "success": False,
            "error": result.get('error', result.get('message', 'Order validation failed')),
            "layer": result.get('layer', 'unknown'),
            "details": result,
            "message": result.get('message', 'Please fix the errors and try again.')
        }), 400
    
    order_summary = result.get('order_summary', {})
    send_approval_email(
        data.get('email', ''),
        filename, 
        f"Accepted - Order Total: {order_summary.get('price', 'N/A')}"
    )
    
    return jsonify({
        "success": True,
        "message": "Order validated and submitted successfully! All guardrails passed.",
        "order_summary": order_summary,
        "reasoning": result.get('reasoning', [])
    })

@app.route('/validate-order', methods=['POST'])
def validate_order():
    """Validate order without submitting."""
    if not agent:
        return jsonify({"error": "Agent not available"}), 500
    
    data = request.json or {}
    
    filename = data.get('filename', '')
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return jsonify({
            "valid": False,
            "error": "File not found. Please upload a file first."
        }), 400
    
    order_data = {
        'email': data.get('email', ''),
        'name': data.get('name', ''),
        'size': data.get('size', ''),
        'paper': data.get('paper', '100lb Matte'),
        'quantity': data.get('quantity', 1),
        'file_path': file_path,
        'filename': filename
    }
    
    result = agent.process_order(order_data)
    return jsonify(result)
