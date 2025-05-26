#!/bin/bash

# Help message
usage() {
  echo "Usage: $0 [-f] [-b]"
  echo "Options:"
  echo "  -f  Tail frontend logs"
  echo "  -b  Tail backend logs"
  exit 1
}

# Check if no arguments are passed
if [ $# -eq 0 ]; then
  usage
fi

# Parse options
while getopts "fb" opt; do
  case $opt in
    f)
      echo "📡 Tailing Frontend Logs..."
      render logs -r srv-d0p7d68dl3ps73aho80g --tail --output text
      ;;
    b)
      echo "📡 Tailing Backend Logs..."
      render logs -r srv-d0p3ui0dl3ps73afh78g --tail --output text
      ;;
    *)
      usage
      ;;
  esac
done