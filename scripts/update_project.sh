#!/bin/bash
# update_project.sh
# Usage: ./update_project.sh <branch-or-tag>
# Example: ./update_project.sh main
#          ./update_project.sh 2.0.0

set -euo pipefail
# -e: exit on error
# -u: treat unset vars as errors
# -o pipefail: catch errors in piped commands

# Trap any unexpected error
trap 'echo "Error on line $LINENO while executing: $BASH_COMMAND" >&2; exit 1' ERR

REF=${1:-}

if [ -z "$REF" ]; then
    echo "Error: No branch or tag specified." >&2
    echo "Usage: $0 <branch-or-tag>" >&2
    exit 1
fi

cd "$(dirname "$0")" || { echo "Failed to change directory." >&2; exit 1; }

echo "Fetching all branches and tags..."
git fetch --all --tags || { echo "Git fetch failed." >&2; exit 1; }

if git rev-parse "refs/tags/$REF" >/dev/null 2>&1; then
    echo "🏷️  Checking out tag: $REF"
    git checkout "tags/$REF" -f || { echo "Failed to checkout tag $REF." >&2; exit 1; }
else
    echo "Checking out branch: $REF"
    git checkout "$REF" || { echo "Failed to checkout branch $REF." >&2; exit 1; }
    git reset --hard "origin/$REF" || { echo "Failed to reset branch $REF." >&2; exit 1; }
fi

echo "Checked out '$REF' successfully."

if [ -f ../requirements.txt ]; then
    echo "Installing dependencies (force reinstall)..."
    pip install --upgrade pip || { echo "pip upgrade failed." >&2; exit 1; }
    pip install --upgrade -r ../requirements.txt || { echo "pip install failed." >&2; exit 1; }
    echo "Dependencies installed."
else
    echo "No requirements.txt found — skipping pip install." >&2; exit 1;
fi

echo "Update complete."
exit 0