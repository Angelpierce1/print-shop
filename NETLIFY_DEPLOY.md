# Netlify Deployment Guide

## ⚠️ Important Limitations

Netlify Functions have several limitations that affect this Flask application:

1. **File Upload Limits**: 6MB for functions, 10MB for forms
2. **Execution Time**: 10 seconds (free), 26 seconds (pro)
3. **No Persistent Storage**: Files in `/tmp` are ephemeral
4. **Python Runtime**: Limited Python packages support

## Recommended Alternatives

For a Flask app with file uploads and image processing, consider:

1. **Render** (Recommended) - Free tier, supports Flask, file uploads
2. **Railway** - Easy deployment, good for Python apps
3. **Heroku** - Traditional option, paid plans available
4. **Fly.io** - Good for Docker-based deployments

## Netlify Deployment Steps

If you still want to deploy to Netlify:

### Option 1: Deploy Static Frontend Only

1. **Build static version:**
   ```bash
   # The templates/index.html can be served as static
   ```

2. **Deploy to Netlify:**
   ```bash
   npm install -g netlify-cli
   netlify login
   netlify init
   netlify deploy --prod
   ```

### Option 2: Use Netlify Functions (Limited)

The functions are set up but have limitations:

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login:**
   ```bash
   netlify login
   ```

3. **Initialize:**
   ```bash
   netlify init
   ```

4. **Deploy:**
   ```bash
   netlify deploy --prod
   ```

### Option 3: Hybrid Approach (Recommended for Netlify)

1. **Frontend on Netlify** (static HTML/JS)
2. **Backend API on Render/Railway** (Flask app)
3. **CORS configured** between them

## Better Alternative: Render Deployment

For full functionality, use Render:

### Quick Deploy to Render

1. **Create `render.yaml`:**
   ```yaml
   services:
     - type: web
       name: print-shop
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: python app.py
       envVars:
         - key: PORT
           value: 5000
   ```

2. **Deploy:**
   - Push to GitHub
   - Connect to Render
   - Auto-deploy

## Netlify Configuration

The `netlify.toml` file is configured with:
- Function redirects
- Static file serving
- SPA fallback

However, **file uploads won't work properly** due to Netlify's limitations.

## Recommendation

**Use Render or Railway** for this application because:
- ✅ Full Flask support
- ✅ File uploads work
- ✅ Persistent storage
- ✅ No execution time limits
- ✅ Free tier available

Would you like me to set up Render deployment instead?

