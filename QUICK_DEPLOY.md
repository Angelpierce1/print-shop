# 🚀 Quick Deployment Guide

## Your GitHub Repo
✅ Already connected: `https://github.com/Angelpierce1/print-shop.git`

## Deploy to Streamlit Cloud (Recommended - FREE)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"Sign in"** (use your GitHub account)
3. Click **"New app"**
4. Select repository: `Angelpierce1/print-shop`
5. Branch: `main`
6. Main file: `app.py`
7. Click **"Deploy"**

### Step 3: Share with Client
Your app will be live at: `https://print-shop.streamlit.app` (or similar)

---

## Alternative: Railway (If you need PDF support)

Railway supports system dependencies like poppler.

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Select your `print-shop` repository
6. Railway will auto-detect and deploy

---

## Note About Lovable

Lovable is designed for React/Next.js applications, not Streamlit apps. For Streamlit apps, use:
- **Streamlit Cloud** (easiest, free)
- **Railway** (supports system deps)
- **Render** (good alternative)

---

## Quick Commands

```bash
# Commit and push
git add .
git commit -m "Deploy Print Shop app"
git push origin main

# Then deploy on Streamlit Cloud (see steps above)
```

---

## After Deployment

Your client can access the app at the Streamlit Cloud URL. The app includes:
- ✅ Image quality checking
- ✅ HEIC to JPG conversion
- ⚠️ PDF processing (may not work on Streamlit Cloud - use Railway for full PDF support)






