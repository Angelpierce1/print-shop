# Deployment Guide

## Option 1: Streamlit Cloud (Recommended - Free & Easy)

Streamlit Cloud is the easiest way to deploy Streamlit apps for free.

### Steps:

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Note:** PDF processing requires poppler-utils which may not be available on Streamlit Cloud. Consider using alternative PDF libraries or disable PDF features for cloud deployment.

### Quick Deploy URL:
After deployment, you'll get a URL like: `https://your-app-name.streamlit.app`

---

## Option 2: Railway (Supports System Dependencies)

Railway can handle system dependencies like poppler.

### Steps:

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login and Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Add Environment Variables:**
   - Set `PORT=8501` if needed

---

## Option 3: Render

### Steps:

1. Create a `render.yaml` file (see below)
2. Connect your GitHub repo to Render
3. Deploy automatically

---

## Option 4: Heroku

### Steps:

1. **Create Procfile:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

---

## Important Notes:

- **PDF Support:** Streamlit Cloud doesn't support system dependencies like poppler. For PDF features, use Railway, Render, or Heroku.
- **File Storage:** Uploaded files are temporary. Consider using cloud storage (S3, etc.) for production.
- **Environment Variables:** Add any API keys or secrets as environment variables in your deployment platform.

---

## Quick Test Before Deploying:

```bash
# Test locally
streamlit run app.py
```

Make sure everything works before deploying!



