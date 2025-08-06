#!/bin/bash

# Modern360 Assessment Platform - GitHub Push Script
echo "🚀 Modern360 Assessment Platform - GitHub Push Script"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please run this from the project root."
    exit 1
fi

# Get GitHub repository URL from user
echo ""
echo "📝 Please provide your GitHub repository URL:"
echo "Example: https://github.com/yourusername/modern360-assessment.git"
read -p "Repository URL: " repo_url

if [ -z "$repo_url" ]; then
    echo "❌ Repository URL is required"
    exit 1
fi

# Check if remote origin exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "🔄 Updating existing remote origin..."
    git remote set-url origin "$repo_url"
else
    echo "➕ Adding remote origin..."
    git remote add origin "$repo_url"
fi

# Add all files and commit
echo "📦 Adding files to git..."
git add .

echo "💾 Creating commit..."
git commit -m "Deploy Modern360 Assessment Platform to Render.com" || echo "No changes to commit"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🌐 Next Steps:"
echo "1. Go to render.com and create a new Web Service"
echo "2. Connect your GitHub repository: $(basename "$repo_url" .git)"
echo "3. Follow the deployment guide in DEPLOY_GUIDE.md"
echo ""
echo "📖 Deployment Guide: DEPLOY_GUIDE.md"
echo "🔗 Your repository: $repo_url"
