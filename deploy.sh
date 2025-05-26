#!/bin/bash

echo "🚀 Starting deployment process..."
echo "--------------------------------"

# Activate virtual environment
source venv/bin/activate

# Run tests before deploying (verbose mode)
echo "🔍 Running tests..."
pytest -v --disable-warnings test_api.py

# If tests fail, stop deployment
if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Fix issues before deploying."
    exit 1
fi

echo "✅ All tests passed! Proceeding with deployment..."

# Show files to be committed
echo "📂 Files to be committed:"
git status --short  # ✅ Displays modified and new files

# Add files to staging
git add .

# Commit changes with timestamp
commit_message="Auto-deploy: $(date)"
echo "📝 Committing changes: $commit_message"
git commit -m "$commit_message"

# Push to repository
echo "⬆ Pushing to remote..."
git push origin main

# Deploy backend
#echo "🟢 Deploying backend..."
#render deploys create srv-d0p3ui0dl3ps73afh78g --wait

# Deploy frontend
echo "🟢 Deploying frontend..."
render deploys create srv-d0p7d68dl3ps73aho80g --wait

echo "🎉 Deployment successful!"