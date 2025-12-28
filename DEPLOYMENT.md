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

## Option 5: Homebrew (macOS/Linux)

Deploy Print Shop as a Homebrew formula for easy installation on macOS and Linux.

### Prerequisites:

1. **GitHub Repository:** Your code must be in a public GitHub repository
2. **GitHub Release:** Create a tagged release (e.g., v1.0.0)
3. **Homebrew:** Install Homebrew if not already installed: https://brew.sh

### Steps:

1. **Create a GitHub Release:**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```
   Then create a release on GitHub with this tag.

2. **Update the Homebrew Formula:**
   - Open `print-shop.rb`
   - Update the `url` field with your release tarball URL:
     ```ruby
     url "https://github.com/yourusername/print-shop/archive/refs/tags/v1.0.0.tar.gz"
     ```
   - Calculate SHA256 and update:
     ```bash
     curl -L https://github.com/yourusername/print-shop/archive/refs/tags/v1.0.0.tar.gz | shasum -a 256
     ```
   - Update the `sha256` field in `print-shop.rb`

3. **Option A: Create a Homebrew Tap (Recommended)**
   
   Create a new repository: `github.com/yourusername/homebrew-print-shop`
   
   ```bash
   # Create tap repository
   mkdir homebrew-print-shop
   cd homebrew-print-shop
   git init
   
   # Copy formula
   mkdir Formula
   cp ../print-shop/print-shop.rb Formula/print-shop.rb
   
   # Commit and push
   git add Formula/print-shop.rb
   git commit -m "Add print-shop formula"
   git remote add origin https://github.com/yourusername/homebrew-print-shop.git
   git push -u origin main
   ```
   
   Users can then install with:
   ```bash
   brew tap yourusername/print-shop
   brew install print-shop
   ```

4. **Option B: Install Directly from Formula**
   
   ```bash
   brew install --build-from-source ./print-shop.rb
   ```

5. **Usage After Installation:**
   
   ```bash
   # Run the Print Shop app
   print-shop
   
   # Convert HEIC files from command line
   print-shop-convert-heic image.heic output.jpg
   ```

### Quick Setup Script:

Run the setup helper:
```bash
chmod +x setup-homebrew.sh
./setup-homebrew.sh
```

### Updating the Formula:

When releasing a new version:
1. Create a new GitHub release tag
2. Update `url` and `sha256` in `print-shop.rb`
3. Update version number in formula
4. Commit and push to your tap repository

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







