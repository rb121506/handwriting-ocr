# Switching to Google Cloud Vision OCR

This application now supports both **Tesseract OCR** (default) and **Google Cloud Vision OCR**.

## Benefits of Google Cloud Vision OCR

- **Higher Accuracy**: Especially for handwritten text
- **Better Language Support**: Supports 200+ languages
- **Advanced Features**: Detects text orientation, multiple languages in same image
- **No Local Installation**: Cloud-based processing

## Setup Instructions for Google Cloud Vision

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Cloud Vision API** for your project

### 2. Create Service Account Credentials

1. Go to **IAM & Admin** > **Service Accounts**
2. Click **Create Service Account**
3. Give it a name (e.g., "ocr-app")
4. Grant role: **Cloud Vision AI Service Agent**
5. Click **Done**
6. Click on the created service account
7. Go to **Keys** tab
8. Click **Add Key** > **Create New Key**
9. Choose **JSON** format
10. Download the JSON key file

### 3. Configure the Application

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` file:
   ```
   OCR_ENGINE=google
   GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-key.json
   ```

3. Set the environment variable:
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account-key.json"
   $env:OCR_ENGINE="google"
   ```

### 4. Run the Application

```powershell
python app.py
```

## Switching Back to Tesseract

To use Tesseract OCR instead:

1. Set environment variable:
   ```powershell
   $env:OCR_ENGINE="tesseract"
   ```

2. Or edit `.env`:
   ```
   OCR_ENGINE=tesseract
   ```

## Pricing

- Google Cloud Vision: First 1,000 units/month are free, then $1.50 per 1,000 units
- Tesseract: Completely free and open-source

## Current Configuration

By default, the app uses **Tesseract OCR** (free, no API key required).
