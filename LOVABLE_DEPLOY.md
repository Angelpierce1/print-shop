# Deploying to Lovable

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   npm install
   ```

2. **Run Development Server:**
   ```bash
   npm run dev
   ```

3. **Build for Production:**
   ```bash
   npm run build
   ```

## Deploying to Lovable

1. Go to [Lovable.dev](https://lovable.dev)
2. Sign in with your GitHub account
3. Click "New Project"
4. Select "Import from GitHub"
5. Choose your `print-shop` repository
6. Lovable will automatically detect it's a Next.js app and deploy it

## Important Notes

- **HEIC Conversion**: Currently uses client-side conversion. For full HEIC support, you may need to add a server-side Python service or use a cloud API.
- **PDF Processing**: PDF features are not included in this Next.js version. You can add them using libraries like `pdf-lib` or integrate with a Python backend API.
- **Image Processing**: Uses `sharp` for server-side image processing, which is much faster than PIL in Node.js.

## Features Included

✅ Image quality checking (DPI analysis)
✅ Batch image processing
✅ HEIC to JPG conversion (basic)
✅ Modern React/Next.js UI
✅ Responsive design with Tailwind CSS

## Missing Features (from Streamlit version)

⚠️ Full PDF processing (requires Python backend or additional setup)
⚠️ Advanced HEIC support (may need additional libraries)

## Next Steps

1. Deploy to Lovable
2. Test all features
3. Add PDF support if needed (consider Python API backend)
4. Enhance HEIC conversion if needed



