# Quick Deploy to Netlify

## ⚠️ Important Warning

**Netlify has significant limitations for this Flask application:**
- File uploads are limited (6MB max)
- No persistent file storage
- Execution time limits (10-26 seconds)
- Python package limitations

**Recommended:** Use **Render** or **Railway** instead for full functionality.

## If You Still Want Netlify:

### Method 1: Using Netlify CLI

```bash
# Install Netlify CLI (if not installed)
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize (first time only)
netlify init

# Deploy
netlify deploy --prod
```

### Method 2: Using Git Integration

1. Push your code to GitHub
2. Go to [Netlify Dashboard](https://app.netlify.com)
3. Click "New site from Git"
4. Select your repository
5. Build settings:
   - Build command: `echo "No build needed"`
   - Publish directory: `.`
6. Deploy!

## Better Alternative: Render (Recommended)

Render is much better suited for Flask apps with file uploads:

### Quick Deploy to Render:

1. **Push to GitHub** (if not already)
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Go to Render Dashboard**
   - Visit [render.com](https://render.com)
   - Sign up/login
   - Click "New +" → "Web Service"

3. **Connect GitHub Repo**
   - Select your repository
   - Render will auto-detect `render.yaml`

4. **Deploy!**
   - Render will automatically:
     - Install dependencies from `requirements.txt`
     - Start the Flask app
     - Provide a public URL

### Render Configuration

The `render.yaml` file is already configured:
- Python environment
- Flask app startup
- Port configuration

## Railway Alternative

Railway is also excellent for Flask apps:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

## Comparison

| Feature | Netlify | Render | Railway |
|---------|---------|--------|---------|
| File Uploads | ❌ Limited | ✅ Full | ✅ Full |
| Flask Support | ⚠️ Functions Only | ✅ Full | ✅ Full |
| Persistent Storage | ❌ No | ✅ Yes | ✅ Yes |
| Free Tier | ✅ Yes | ✅ Yes | ✅ Yes |
| Ease of Use | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## Recommendation

**Use Render** for this application. It's:
- ✅ Free tier available
- ✅ Full Flask support
- ✅ File uploads work perfectly
- ✅ Easy deployment
- ✅ Auto-deploy from Git

The `render.yaml` is already configured and ready to go!

