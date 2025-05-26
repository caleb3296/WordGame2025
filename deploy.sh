#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run tests before deployment
pytest test_api.py

# If tests fail, stop deployment
if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Fix issues before deploying."
    exit 1
fi

# Commit and push changes
git add .
git commit -m "Auto-deploy: $(date)"
git push origin main

# Deploy backend
#render deploys create srv-d0p3ui0dl3ps73afh78g --wait

# Deploy frontend
render deploys create srv-d0p7d68dl3ps73aho80g --wait