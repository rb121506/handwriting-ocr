# Using Google Gemini API for OCR

Google Gemini is a powerful multimodal AI that excels at extracting text from images, including handwritten text.

## Benefits of Gemini for OCR

- **Excellent Handwriting Recognition**: Superior accuracy for handwritten text
- **Context Understanding**: Can understand and preserve formatting
- **Easy Setup**: Just needs an API key (no service account required)
- **Generous Free Tier**: 1500 requests per day for free
- **Fast Processing**: Quick response times

## Setup Instructions

### 1. Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Copy your API key

### 2. Configure the Application

**Option A: Using Environment Variables (Recommended)**

Set the environment variables in PowerShell:

```powershell
$env:OCR_ENGINE="gemini"
$env:GEMINI_API_KEY="your_api_key_here"
```

**Option B: Using .env File**

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` file:
   ```
   OCR_ENGINE=gemini
   GEMINI_API_KEY=your_api_key_here
   ```

### 3. Run the Application

```powershell
python app.py
```

The app will now use Gemini for OCR!

## Switching Between OCR Engines

You can easily switch between different OCR engines:

### Use Gemini (Recommended for Handwriting)
```powershell
$env:OCR_ENGINE="gemini"
$env:GEMINI_API_KEY="your_api_key_here"
```

### Use Google Cloud Vision
```powershell
$env:OCR_ENGINE="google"
$env:GOOGLE_APPLICATION_CREDENTIALS="path\to\credentials.json"
```

### Use Tesseract (Free, Local)
```powershell
$env:OCR_ENGINE="tesseract"
```

## Pricing

- **Free Tier**: 1,500 requests per day
- **Paid**: $0.00025 per image (after free tier)

For most personal use cases, the free tier is more than sufficient!

## Comparison

| Feature | Gemini | Google Cloud Vision | Tesseract |
|---------|--------|-------------------|-----------|
| Handwriting Accuracy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Setup Difficulty | Easy | Medium | Easy |
| Free Tier | 1,500/day | 1,000/month | Unlimited |
| Internet Required | Yes | Yes | No |
| Speed | Fast | Fast | Very Fast |

## Troubleshooting

### "GEMINI_API_KEY environment variable not set"
Make sure you've set the API key:
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

### Rate Limit Exceeded
If you exceed the free tier limits, wait 24 hours or upgrade to a paid plan.

### API Key Invalid
- Verify your API key is correct
- Make sure it's from [Google AI Studio](https://aistudio.google.com/apikey)
- Check that the API is enabled in your Google Cloud project
