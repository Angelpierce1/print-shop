#!/bin/bash
# Netlify Deployment Script

echo "🚀 Deploying to Netlify..."

# Check if netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

# Login check
echo "📋 Checking Netlify login..."
netlify status || netlify login

# Deploy
echo "📦 Deploying..."
netlify deploy --prod

echo "✅ Deployment complete!"
echo "⚠️  Note: Netlify Functions have limitations for file uploads."
echo "💡 Consider using Render or Railway for full functionality."

