#!/bin/bash
# Setup script for Homebrew deployment

set -e

echo "🍺 Print Shop - Homebrew Setup"
echo "=============================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed."
    echo "Please install Homebrew first: https://brew.sh"
    exit 1
fi

echo "✅ Homebrew is installed"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "⚠️  Not a git repository. Initializing..."
    git init
    git branch -M main
    echo "✅ Git repository initialized"
    echo ""
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo "⚠️  No GitHub remote found!"
    echo ""
    echo "To deploy to Homebrew, you need to:"
    echo "1. Create a GitHub repository"
    echo "2. Create a release tag (e.g., v1.0.0)"
    echo "3. Update the URL and SHA256 in print-shop.rb"
    echo ""
    read -p "Do you have a GitHub repo URL? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your GitHub repo URL: " repo_url
        git remote add origin "$repo_url"
        echo "✅ Remote added!"
    fi
fi

echo ""
echo "📋 Next steps for Homebrew deployment:"
echo ""
echo "1. Create a GitHub release:"
echo "   - Tag your release: git tag -a v1.0.0 -m 'Release v1.0.0'"
echo "   - Push tag: git push origin v1.0.0"
echo "   - Create a release on GitHub with the tag"
echo ""
echo "2. Update print-shop.rb:"
echo "   - Set the correct URL to your release tarball"
echo "   - Calculate SHA256: shasum -a 256 <release-tarball>"
echo "   - Update the sha256 field in print-shop.rb"
echo ""
echo "3. Create a Homebrew tap (optional):"
echo "   - Create a new repo: github.com/yourusername/homebrew-print-shop"
echo "   - Copy print-shop.rb to: homebrew-print-shop/Formula/print-shop.rb"
echo ""
echo "4. Install from tap:"
echo "   brew tap yourusername/print-shop"
echo "   brew install print-shop"
echo ""
echo "Or install directly:"
echo "   brew install --build-from-source ./print-shop.rb"
echo ""
echo "✨ Setup complete!"

