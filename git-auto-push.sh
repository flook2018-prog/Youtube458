#!/bin/bash
# Auto-commit and push to GitHub
# Usage: ./git-auto-push.sh "commit message"

if [ -z "$1" ]; then
    echo "❌ Error: Provide commit message"
    echo "Usage: ./git-auto-push.sh 'Your commit message'"
    exit 1
fi

echo "📦 Staging changes..."
git add -A

echo "📝 Committing..."
git commit -m "$1"

echo "⬆️  Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Pushed successfully!"
else
    echo "❌ Push failed!"
    exit 1
fi
