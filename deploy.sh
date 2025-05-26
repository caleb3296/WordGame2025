#!/bin/bash

echo "🚀 Starting deployment process..."
echo "--------------------------------"

# Activate virtual environment
source venv/bin/activate

# Ensure logs directory exists
mkdir -p logs

# 🔄 Refresh dependencies
echo "🔄 Updating dependencies..."
pip freeze > requirements.txt

# ✅ Run tests before deploying
echo "🔍 Running tests..."
pytest -v --disable-warnings test_api.py | tee logs/test_output.log
TEST_EXIT=$?

if [ $TEST_EXIT -ne 0 ]; then
    echo "❌ Tests failed! Fix issues before deploying."
    exit 1
else
    echo "✅ All tests passed! Proceeding with deployment..."
fi

# ✅ Show files to be committed
echo "📂 Files to be committed:"
git status --short

# ✅ Commit & push changes
git add .
commit_message="Auto-deploy: $(date)"
echo "📝 Committing changes: $commit_message"
git commit -m "$commit_message"
echo "⬆ Pushing to remote..."
git push origin main | tee logs/git_push.log

# ✅ Deploy backend & immediately start tailing logs
echo "🟢 Deploying backend..."
DEPLOY_ID=$(echo "y" | render deploys create srv-d0p3ui0dl3ps73afh78g --clear-cache --wait | tee logs/backend_deploy.log | awk '/Deploy dep-/ {print $NF}')
echo "📡 Backend deployment ID: $DEPLOY_ID"

# ✅ Stream live logs without locking the terminal
render logs -r srv-d0p3ui0dl3ps73afh78g --tail | tee logs/backend_live.log &

# ✅ Deploy frontend & immediately start tailing logs
echo "🟢 Deploying frontend..."
DEPLOY_ID=$(echo "y" | render deploys create srv-d0p7d68dl3ps73aho80g --clear-cache --wait | tee logs/frontend_deploy.log | awk '/Deploy dep-/ {print $NF}')
echo "📡 Frontend deployment ID: $DEPLOY_ID"

render logs -r srv-d0p7d68dl3ps73aho80g --tail | tee logs/frontend_live.log &

echo "🎉 Deployment successful!"