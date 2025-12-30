import os
import smtplib
from flask import Flask, render_template, request, jsonify, url_for
from PIL import Image
from pillow_heif import register_heif_opener
from pdf2image import convert_from_bytes
from email.mime.text import MIMEText
from agent import PrintShopAgent

# Register HEIC opener for Pillow
register_heif_opener()

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the AI Order Guardrail Agent
agent = PrintShopAgent()

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
    print(f"Body: Your design '{filename}' is {status}. Please click here to approve: http://localhost:5000/approve/{filename}")
    print("-------------------------------")
    return True

@app.route('/')
def index():
    return render_template('index.html', sizes=PRINT_SIZES)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = file.filename.lower()
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # --- CONVERSION LOGIC ---
    img = None
    
    if filename.endswith('.pdf'):
        # Convert first page of PDF to JPG
        images = convert_from_bytes(file.read())
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
    # We pass the pixel dimensions back to the frontend
    # The frontend will check these pixels against the selected physical inches
    width_px, height_px = img.size
    
    return jsonify({
        "url": url_for('static', filename=f'uploads/{os.path.basename(filepath)}'),
        "width": width_px,
        "height": height_px,
        "filename": os.path.basename(filepath)
    })

@app.route('/submit-order', methods=['POST'])
def submit_order():
    """
    Submit order with AI Order Guardrail validation.
    Uses the three-layer guardrail system to catch errors before human review.
    """
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
    
    if not result['valid']:
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
    send_approval_email(
        data['email'], 
        filename, 
        f"Accepted - Order Total: {result['order_summary']['price']}"
    )
    
    # Return success with order summary
    return jsonify({
        "success": True,
        "message": "Order validated and submitted successfully! All guardrails passed.",
        "order_summary": result['order_summary'],
        "reasoning": result.get('reasoning', [])
    })


@app.route('/validate-order', methods=['POST'])
def validate_order():
    """
    Validate order without submitting (preview/check only).
    Useful for real-time validation feedback.
    """
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
