#!/bin/bash
# Script to help create a Homebrew release

set -e

VERSION=${1:-"1.0.0"}
REPO_URL=${2:-""}

if [ -z "$REPO_URL" ]; then
    echo "Usage: $0 <version> <github-repo-url>"
    echo "Example: $0 v1.0.0 https://github.com/yourusername/print-shop"
    exit 1
fi

echo "🍺 Creating Homebrew Release for Print Shop"
echo "==========================================="
echo ""
echo "Version: $VERSION"
echo "Repository: $REPO_URL"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Please initialize git first."
    exit 1
fi

# Check if tag exists
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo "✅ Tag $VERSION already exists"
else
    echo "📝 Creating tag $VERSION..."
    read -p "Create tag $VERSION? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -a "$VERSION" -m "Release $VERSION"
        echo "✅ Tag created"
        echo ""
        read -p "Push tag to remote? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git push origin "$VERSION"
            echo "✅ Tag pushed"
        fi
    fi
fi

# Construct tarball URL
TARBALL_URL="${REPO_URL}/archive/refs/tags/${VERSION}.tar.gz"

echo ""
echo "📦 Release Information:"
echo "======================"
echo "Tarball URL: $TARBALL_URL"
echo ""

# Download and calculate SHA256
echo "📥 Downloading tarball to calculate SHA256..."
TEMP_FILE=$(mktemp)
curl -L -o "$TEMP_FILE" "$TARBALL_URL" 2>/dev/null || {
    echo "❌ Failed to download tarball. Make sure:"
    echo "   1. The tag $VERSION exists on GitHub"
    echo "   2. A release has been created with this tag"
    echo "   3. The repository URL is correct"
    exit 1
}

SHA256=$(shasum -a 256 "$TEMP_FILE" | awk '{print $1}')
rm "$TEMP_FILE"

echo "✅ SHA256: $SHA256"
echo ""

# Update print-shop.rb
echo "📝 Updating print-shop.rb..."
FORMULA_FILE="print-shop.rb"

if [ ! -f "$FORMULA_FILE" ]; then
    echo "❌ print-shop.rb not found!"
    exit 1
fi

# Update URL
sed -i.bak "s|url \".*\"|url \"$TARBALL_URL\"|" "$FORMULA_FILE"

# Update SHA256
sed -i.bak "s|sha256 \".*\"|sha256 \"$SHA256\"|" "$FORMULA_FILE"

# Update version
sed -i.bak "s|version \".*\"|version \"$VERSION\"|" "$FORMULA_FILE"

rm -f "${FORMULA_FILE}.bak"

echo "✅ print-shop.rb updated!"
echo ""

echo "📋 Next Steps:"
echo "============="
echo ""
echo "1. Review the updated print-shop.rb file"
echo "2. Create a Homebrew tap repository:"
echo "   - Create: github.com/yourusername/homebrew-print-shop"
echo "   - Copy print-shop.rb to: Formula/print-shop.rb"
echo ""
echo "3. Or test locally:"
echo "   brew install --build-from-source ./print-shop.rb"
echo ""
echo "4. Users can install with:"
echo "   brew tap yourusername/print-shop"
echo "   brew install print-shop"
echo ""
echo "✨ Done!"

