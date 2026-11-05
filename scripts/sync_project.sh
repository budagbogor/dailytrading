#!/usr/bin/env bash
# Run locally from the COMPLETE QuantSyariah source directory.
# Requires git and a GitHub account with write access (gh auth login or git credential manager).
set -euo pipefail
REPO_URL="https://github.com/budagbogor/dailytrading.git"
BRANCH="main"
python3 scripts/preflight.py
python3 -m unittest discover -s tests -q
if [[ -e .env || -e local.properties ]]; then
  echo "Refusing to publish local credentials" >&2
  exit 1
fi
if [[ ! -d .git ]]; then
  git init
  git branch -M "$BRANCH"
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "$REPO_URL"
fi
if [[ "$(git remote get-url origin)" != "$REPO_URL" ]]; then
  echo "Unexpected origin remote; refusing to push" >&2
  exit 1
fi
git fetch origin "$BRANCH"
git checkout -B "$BRANCH" "origin/$BRANCH"
git add app backend tests scripts .github README.md settings.gradle.kts build.gradle.kts .gitignore
git diff --cached --check
if git diff --cached --quiet; then
  echo "No source changes to push"
  exit 0
fi
git commit -m "Sync complete QuantSyariah source tree"
git push origin "$BRANCH"
echo "Pushed source tree; inspect GitHub Actions for APK build results."
