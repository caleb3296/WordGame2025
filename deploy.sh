#!/bin/bash

echo "🚀 Starting deployment process..."
echo "--------------------------------"

# Activate virtual environment
source venv/bin/activate

# Run tests before deploying (verbose mode)
echo "🔍 Running tests..."
pytest -v --disable-warnings test_api.py | tee logs/test_output.log
TEST_EXIT=$?  # ✅ Captures pytest exit code

if [ $TEST_EXIT -ne 0 ]; then
    echo "❌ Tests failed! Fix issues before deploying."
    exit 1
else
    echo "✅ All tests passed! Proceeding with deployment..."
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
git push origin main | tee logs/git_push.log

# Deploy backend with verbose logs
echo "🟢 Deploying backend..."
render deploys create srv-d0p3ui0dl3ps73afh78g --wait | tee logs/backend_deploy.log

# Deploy frontend with verbose logs
echo "🟢 Deploying frontend..."
render deploys create srv-d0p7d68dl3ps73aho80g --wait | tee logs/frontend_deploy.log

echo "🎉 Deployment successful!"