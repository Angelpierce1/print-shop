# Print Shop - Image Quality Checker

A Streamlit web application for checking image print quality. Upload images to verify they meet professional printing standards (300 DPI minimum).

## Features

- 📤 **Single Image Upload**: Upload and check individual images
- 📁 **Batch Processing**: Process multiple images at once
- 📊 **Quality Analysis**: Check DPI, dimensions, and print suitability
- 🔄 **HEIC to JPG Conversion**: Convert HEIC/HEIF images to JPG format
- 📄 **PDF Processing**: Convert PDF pages to images and check quality
- 💾 **Image Management**: Save images to local directory
- 🎨 **Modern UI**: Clean, user-friendly interface

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. **For PDF support**, install poppler-utils (required by pdf2image):
   - **macOS:** `brew install poppler`
   - **Ubuntu/Debian:** `sudo apt-get install poppler-utils`
   - **Windows:** Download from [poppler-windows releases](https://github.com/oschwartz10612/poppler-windows/releases)

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser to the URL shown (typically `http://localhost:8501`)

3. Upload images and check their print quality!

## HEIC to JPG Conversion

The app includes built-in HEIC/HEIF to JPG conversion:

### Web Interface
1. Go to the **"🔄 HEIC Converter"** tab in the Streamlit app
2. Upload HEIC/HEIF files
3. Adjust JPG quality (default: 95)
4. Click "Convert All HEIC Files"
5. Download or auto-save converted JPG files

### Command Line
You can also use the standalone converter script:

```bash
# Convert a single HEIC file
python convert_heic.py image.heic

# Specify output file
python convert_heic.py image.heic output.jpg

# Set custom quality (1-100)
python convert_heic.py image.heic output.jpg 90
```

### Automatic Conversion
When uploading HEIC files in the "Upload & Check" or "Batch Process" tabs, you can enable automatic conversion to JPG when saving files.

## PDF Processing

The app can convert PDF pages to images for quality checking:

1. Go to the **"📄 PDF Processor"** tab
2. Upload a PDF file
3. Configure settings:
   - **DPI**: Resolution for conversion (72-600, default 300)
   - **Pages**: Select all pages, first page only, or custom range
4. Click "Convert PDF to Images"
5. View converted images with quality analysis
6. Download individual pages or auto-save all

### PDF Requirements
- Requires `poppler-utils` to be installed on your system
- See installation instructions above

## How It Works

- **High Quality**: Images with ≥ 300 DPI at the target print width
- **Low Quality**: Images with < 300 DPI (may appear pixelated when printed)

The app checks both:
- **Metadata DPI**: DPI information embedded in the image file
- **Effective DPI**: Calculated from pixel dimensions and target print size

## Requirements

- Python 3.7+
- Streamlit
- Pillow (PIL)
- pillow-heif (for HEIC/HEIF support)
- pdf2image (for PDF processing)
- PyPDF2 (for PDF metadata)
- poppler-utils (system dependency for PDF processing)
- pymp (optional, for parallel processing in init.py)

## Supported File Formats

- **Images (Input)**: JPG, PNG, GIF, BMP, TIFF, HEIC, HEIF
- **PDF (Input)**: PDF files (converted to images)
- **Output**: JPG (for HEIC/PDF conversions), Original format (for other images)



