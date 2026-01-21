import os
import logging
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import cv2
import numpy as np
from pdf2image import convert_from_path
import tempfile
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image):
    """
    Preprocess image for better OCR accuracy.
    
    Args:
        image: PIL Image or numpy array
        
    Returns:
        Preprocessed image as numpy array
    """
    # Convert PIL Image to numpy array if needed
    if isinstance(image, Image.Image):
        img = np.array(image)
    else:
        img = image
    
    # Convert to grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img
    
    # Apply Gaussian blur for noise reduction
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding for better binarization
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    # Apply morphological operations to reduce noise
    kernel = np.ones((1, 1), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
    
    # Enhance contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(morph)
    
    return enhanced

def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Extracted text as string
    """
    try:
        # Load image
        image = Image.open(image_path)
        
        # Preprocess image
        processed = preprocess_image(image)
        
        # Perform OCR with custom configuration for handwriting
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed, config=custom_config)
        
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from image: {str(e)}")
        raise

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file by converting pages to images.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text from all pages as string
    """
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        
        all_text = []
        for i, image in enumerate(images):
            logger.info(f"Processing page {i + 1} of {len(images)}")
            
            # Preprocess image
            processed = preprocess_image(image)
            
            # Perform OCR
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(processed, config=custom_config)
            
            if text.strip():
                all_text.append(f"--- Page {i + 1} ---\n{text.strip()}")
        
        return '\n\n'.join(all_text)
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

def cleanup_old_files():
    """Remove files older than 1 hour from uploads folder."""
    try:
        upload_folder = app.config['UPLOAD_FOLDER']
        current_time = time.time()
        
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                # Remove files older than 1 hour (3600 seconds)
                if file_age > 3600:
                    os.remove(file_path)
                    logger.info(f"Removed old file: {filename}")
    except Exception as e:
        logger.error(f"Error cleaning up old files: {str(e)}")

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and OCR processing.
    
    Returns:
        JSON response with extracted text or error message
    """
    # Clean up old files before processing new upload
    cleanup_old_files()
    
    # Check if file is present in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload JPEG, JPG, PNG, or PDF files.'}), 400
    
    filepath = None
    try:
        # Secure the filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file
        file.save(filepath)
        logger.info(f"File saved: {filename}")
        
        # Extract text based on file type
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension == 'pdf':
            extracted_text = extract_text_from_pdf(filepath)
        else:
            extracted_text = extract_text_from_image(filepath)
        
        # Calculate statistics
        word_count = len(extracted_text.split())
        char_count = len(extracted_text)
        
        # Clean up the uploaded file
        os.remove(filepath)
        logger.info(f"File processed and removed: {filename}")
        
        return jsonify({
            'success': True,
            'text': extracted_text,
            'word_count': word_count,
            'char_count': char_count
        })
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        
        # Clean up file if it exists
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'error': f'Error processing file: {str(e)}'
        }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

if __name__ == '__main__':
    # Get debug mode from environment variable (default: False for production)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
