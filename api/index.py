"""Flask app for Print Shop AI Order Guardrail - Vercel serverless function."""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from flask import Flask, render_template, request, jsonify, url_for
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
from email.mime.text import MIMEText

# Import agent - adjust path as needed
try:
    from agent import PrintShopAgent
except ImportError:
    # Fallback if agent is in different location
    PrintShopAgent = None

# Initialize Flask app - MUST be named 'app' for Vercel
app = Flask(__name__, 
            template_folder=str(Path(__file__).parent.parent / 'templates'),
            static_folder=str(Path(__file__).parent.parent / 'static'))

# For Vercel serverless, we can't use file uploads the same way
# Uploads would need to be handled via cloud storage (S3, etc.)
UPLOAD_FOLDER = '/tmp/uploads'  # Use /tmp for serverless
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the AI Order Guardrail Agent
agent = PrintShopAgent() if PrintShopAgent else None

# Standard Print Sizes (Inches)
PRINT_SIZES = {
    "3x5": (3, 5), "4x6": (4, 6), "5x7": (5, 7),
    "8x10": (8, 10), "8.5x11": (8.5, 11), "11x14": (11, 14),
    "11x17": (11, 17), "12x18": (12, 18), "13x19": (13, 19)
}

MIN_DPI = 225

def send_approval_email(email, filename, status):
    """Simulates sending an email"""
    # In production, use SendGrid, SES, or real SMTP credentials
    print(f"--- EMAIL SENT TO {email} ---")
    print(f"Subject: Order Update - {status}")
    print(f"Body: Your design '{filename}' is {status}.")
    print("-------------------------------")
    return True

@app.route('/')
@app.route('/api')
@app.route('/api/index')
def index():
    """Root endpoint - returns API info or serves HTML template."""
    # For API endpoint, return JSON
    if request.path.startswith('/api'):
        return jsonify({
            "success": True,
            "message": "Print Shop AI Order Guardrail API",
            "endpoints": {
                "upload": "/api/upload",
                "submit_order": "/api/submit-order",
                "validate_order": "/api/validate-order"
            }
        })
    # For root, try to serve template (may not work in serverless)
    try:
        return render_template('index.html', sizes=PRINT_SIZES)
    except:
        return jsonify({
            "message": "Print Shop API - Use /api endpoints",
            "endpoints": ["/api/upload", "/api/submit-order", "/api/validate-order"]
        })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload file endpoint - Note: File uploads need cloud storage for production."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = file.filename.lower()
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # --- CONVERSION LOGIC ---
    img = None
    
    try:
        if filename.endswith('.pdf'):
            if convert_from_bytes is None:
                return jsonify({"error": "PDF conversion not available"}), 500
            # Convert first page of PDF to JPG
            file_data = file.read()
            images = convert_from_bytes(file_data)
            img = images[0]
            new_filename = filename.replace('.pdf', '.jpg')
            filepath = os.path.join(UPLOAD_FOLDER, new_filename)
            img.save(filepath, 'JPEG')
        elif filename.endswith('.heic'):
            # Convert HEIC to JPG
            img = Image.open(file)
            new_filename = filename.replace('.heic', '.jpg')
            filepath = os.path.join(UPLOAD_FOLDER, new_filename)
            img.save(filepath, "JPEG")
        else:
            # Standard Save
            file.save(filepath)
            img = Image.open(filepath)

        # --- DPI CALCULATION ---
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

@app.route('/api/submit-order', methods=['POST'])
def submit_order():
    """
    Submit order with AI Order Guardrail validation.
    Uses the three-layer guardrail system to catch errors before human review.
    """
    if not agent:
        return jsonify({"error": "Agent not available"}), 500
    
    data = request.json
    
    # Get file path from filename
    filename = data.get('filename', '')
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # Check if file exists (use original if converted)
    if not os.path.exists(file_path):
        # Try to find the file (might have been converted)
        base_name = os.path.splitext(filename)[0]
        for ext in ['.jpg', '.jpeg', '.png', '.pdf']:
            test_path = os.path.join(UPLOAD_FOLDER, base_name + ext)
            if os.path.exists(test_path):
                file_path = test_path
                filename = os.path.basename(test_path)
                break
    
    # Prepare order data for agent
    order_data = {
        'email': data.get('email', ''),
        'name': data.get('name', ''),
        'size': data.get('size', ''),
        'paper': data.get('paper', '100lb Matte'),  # Default paper
        'quantity': data.get('quantity', 1),
        'file_path': file_path,
        'filename': filename
    }
    
    # Process order through AI Agent with guardrails
    result = agent.process_order(order_data)
    
    if not result.get('valid', False):
        # Order failed validation - return error details
        return jsonify({
            "success": False,
            "error": result.get('error', result.get('message', 'Order validation failed')),
            "layer": result.get('layer', 'unknown'),
            "details": result,
            "message": result.get('message', 'Please fix the errors and try again.')
        }), 400
    
    # Order passed all guardrails - proceed with submission
    # Simulate "Accepted" Email
    order_summary = result.get('order_summary', {})
    send_approval_email(
        data.get('email', ''),
        filename, 
        f"Accepted - Order Total: {order_summary.get('price', 'N/A')}"
    )
    
    # Return success with order summary
    return jsonify({
        "success": True,
        "message": "Order validated and submitted successfully! All guardrails passed.",
        "order_summary": order_summary,
        "reasoning": result.get('reasoning', [])
    })


@app.route('/api/validate-order', methods=['POST'])
def validate_order():
    """
    Validate order without submitting (preview/check only).
    Useful for real-time validation feedback.
    """
    if not agent:
        return jsonify({"error": "Agent not available"}), 500
    
    data = request.json
    
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
