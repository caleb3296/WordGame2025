#!/bin/bash

# Custom greeting message
message="Good morning! This is an automated description of my project that you helped me build!! You're a genius at this!! After you read it, I will likely have further instructions!\n\n"

# Extract API endpoints, functions, classes, imports (with the correct exclusion)
summary=$(grep -r --exclude-dir={node_modules,venv} --include=*.py -A 5 -E "^\s*(def|class|import|from|@.*(get|post|put|delete))" .)

# Fetch recent git commits
#gitlog=$(git log --since="2025-05-24" --pretty=format:"%h - %s (%an, %ad)" -n 20)

# Combine outputs & copy to clipboard
printf "%s\n" "$message==== PROJECT SUMMARY ====\n$summary\n\n==== GIT HISTORY ====\n$gitlog" | clip.exe

echo "✅ Copied project details & git history to clipboard. Paste it into Copilot!"