import os
import io
import logging
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from pdf2image import convert_from_path
import time
from google import genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# Initialize Gemini client
gemini_client = None

try:
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    gemini_client = genai.Client(api_key=api_key)
    logger.info("Google Gemini OCR initialized with gemini-2.5-flash")
except Exception as e:
    logger.error(f"Failed to initialize Gemini: {str(e)}")
    raise

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def extract_text_with_gemini(image_input):
    """
    Extract text from an image using Google Gemini API.
    
    Args:
        image_input: Path to the image file, bytes, or PIL Image
        
    Returns:
        Extracted text as string
    """
    try:
        # Load and prepare image
        if isinstance(image_input, Image.Image):
            img = image_input
        elif isinstance(image_input, (bytes, bytearray)):
            img = Image.open(io.BytesIO(image_input))
        else:
            with open(image_input, 'rb') as image_file:
                image_bytes = image_file.read()
            img = Image.open(io.BytesIO(image_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')

        prompt = "Extract only the visible text from this image. Preserve line breaks. If unsure, use [UNK]."

        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, img],
            config={
                "temperature": 0,
                "top_p": 0.1,
                "top_k": 1
            }
        )

        final_text = getattr(response, "text", None) or ""
        return final_text.strip()
    except Exception as e:
        logger.error(f"Error extracting text with Gemini: {str(e)}")
        raise

def extract_text_from_image(image_path):
    """
    Extract text from an image using Gemini API.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Extracted text as string
    """
    return extract_text_with_gemini(image_path)

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
        images = convert_from_path(pdf_path, dpi=300)
        
        all_text = []
        for i, image in enumerate(images):
            logger.info(f"Processing page {i + 1} of {len(images)}")
            
            # Extract text using Gemini
            text = extract_text_with_gemini(image)
            
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
    port = int(os.environ.get('PORT', '5000'))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
