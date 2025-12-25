#!/bin/bash
# Quick deployment script for Print Shop app

echo "🚀 Print Shop Deployment Helper"
echo "================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git branch -M main
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  No GitHub remote found!"
    echo ""
    echo "To deploy, you need to:"
    echo "1. Create a new repository on GitHub"
    echo "2. Run: git remote add origin <your-repo-url>"
    echo "3. Run: git push -u origin main"
    echo ""
    read -p "Do you have a GitHub repo URL? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your GitHub repo URL: " repo_url
        git remote add origin "$repo_url"
        echo "✅ Remote added!"
    fi
fi

# Stage all files
echo ""
echo "📝 Staging files..."
git add .

# Check if there are changes
if git diff --staged --quiet; then
    echo "✅ No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "Deploy Print Shop app"
    echo "✅ Changes committed!"
fi

# Push to remote if it exists
if git remote | grep -q origin; then
    echo ""
    read -p "Push to GitHub? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push -u origin main
        echo ""
        echo "✅ Pushed to GitHub!"
        echo ""
        echo "🌐 Next steps:"
        echo "1. Go to https://share.streamlit.io"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New app'"
        echo "4. Select your repository"
        echo "5. Set main file: app.py"
        echo "6. Click 'Deploy'"
        echo ""
        echo "Your app will be live at: https://your-app-name.streamlit.app"
    fi
fi

echo ""
echo "✨ Done!"



