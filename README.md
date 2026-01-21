# 📝 Handwriting OCR Web Application

A powerful Python-based web application that converts handwritten notes from images (JPEG, JPG, PNG) and PDF files into editable text using advanced OCR (Optical Character Recognition) technology.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)

## ✨ Features

- **Multi-Format Support**: Upload JPEG, JPG, PNG images and PDF documents
- **Drag & Drop Interface**: Intuitive file upload with drag-and-drop functionality
- **Advanced OCR**: Powered by Tesseract OCR with custom handwriting recognition
- **Image Preprocessing**: Automatic image enhancement for better accuracy
  - Grayscale conversion
  - Noise reduction with Gaussian blur
  - Adaptive thresholding
  - Morphological operations
  - Contrast enhancement using CLAHE
- **Multi-Page PDF Support**: Extract text from all pages in PDF documents
- **Interactive Text Editor**: Edit extracted text directly in the browser
- **Quick Actions**:
  - Copy to clipboard with one click
  - Download as .txt file
  - Clear and reset
  - Upload another file
- **Real-time Statistics**: View word and character counts
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Error Handling**: User-friendly error messages and validation
- **Automatic Cleanup**: Temporary files are automatically removed

## 🚀 Demo

The application provides a clean, modern interface where you can:
1. Upload or drag-and-drop your handwritten document
2. Watch as the OCR processes your file
3. View and edit the extracted text
4. Copy or download the results

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **Tesseract OCR**
  - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`
  - Windows: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
- **Poppler** (for PDF support)
  - Ubuntu/Debian: `sudo apt-get install poppler-utils`
  - macOS: `brew install poppler`
  - Windows: Download from [poppler releases](http://blog.alivate.com.au/poppler-windows/)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rb121506/handwriting-ocr.git
cd handwriting-ocr
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Tesseract Installation

```bash
tesseract --version
```

If Tesseract is not found, make sure it's in your system PATH.

## 🎯 Usage

### Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```
   
   For development with debug mode enabled:
   ```bash
   FLASK_DEBUG=true python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Upload a file**:
   - Click the upload area or drag and drop a file
   - Supported formats: JPEG, JPG, PNG, PDF
   - Maximum file size: 16MB

4. **View Results**:
   - Wait for the OCR processing to complete
   - View and edit the extracted text
   - Use the action buttons to copy, download, or clear results

### Configuration

You can modify the following settings in `app.py`:

- **Max file size**: Change `app.config['MAX_CONTENT_LENGTH']` (default: 16MB)
- **Upload folder**: Change `app.config['UPLOAD_FOLDER']` (default: 'uploads')
- **Debug mode**: Set `FLASK_DEBUG=true` environment variable for development
- **OCR engine mode**: Modify the `custom_config` parameter in OCR functions
- **Preprocessing parameters**: Adjust values in the `preprocess_image()` function

## 📁 Project Structure

```
handwriting-ocr/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Documentation (this file)
├── .gitignore            # Git ignore rules
├── static/
│   ├── css/
│   │   └── style.css     # Application styling
│   └── js/
│       └── main.js       # Frontend JavaScript
├── templates/
│   └── index.html        # Main web interface
└── uploads/              # Temporary file storage (auto-created)
```

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **Pytesseract**: Python wrapper for Tesseract OCR
- **OpenCV**: Image preprocessing
- **Pillow**: Image manipulation
- **pdf2image**: PDF to image conversion
- **NumPy**: Numerical operations

### Frontend
- **HTML5**: Structure
- **CSS3**: Modern, responsive styling
- **JavaScript (Vanilla)**: Interactive functionality
- **AJAX**: Asynchronous file upload

## 🔍 How It Works

1. **File Upload**: User uploads an image or PDF file
2. **Validation**: Server validates file type and size
3. **Preprocessing**: 
   - Image is converted to grayscale
   - Noise reduction applied
   - Adaptive thresholding for better contrast
   - Morphological operations to clean up the image
   - Contrast enhancement using CLAHE
4. **OCR Processing**: Tesseract extracts text from the preprocessed image
5. **Results Display**: Extracted text is returned and displayed
6. **User Actions**: User can copy, download, or edit the text

## 📊 OCR Accuracy Tips

For best results:
- Use high-resolution images (at least 300 DPI)
- Ensure good lighting and contrast
- Avoid blurry or distorted images
- Use clear, legible handwriting
- Scan documents straight (not skewed)

## 🐛 Troubleshooting

### "Tesseract not found" error
- Ensure Tesseract is installed and in your system PATH
- On Windows, you may need to set: `pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

### PDF conversion fails
- Install poppler-utils
- Ensure PDF files are not password-protected

### Poor OCR accuracy
- Try preprocessing the image manually before upload
- Increase image resolution
- Ensure the handwriting is clear and legible

### File upload fails
- Check file size (must be under 16MB)
- Verify file format (JPEG, JPG, PNG, or PDF only)
- Ensure upload folder has write permissions

## 🔒 Security Features

- File type validation
- File size limits
- Secure filename handling to prevent directory traversal
- Automatic cleanup of temporary files
- Input sanitization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for the OCR engine
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [OpenCV](https://opencv.org/) for image processing capabilities

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: OCR accuracy depends on image quality and handwriting clarity. Results may vary.