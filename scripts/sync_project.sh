#!/usr/bin/env bash
# Run from a complete QuantSyariah source checkout; never overwrite local source.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 scripts/preflight.py
python3 -m unittest discover -s tests -q
for unsafe in .env local.properties; do
  if [[ -e "$unsafe" ]]; then echo "Refusing to publish $unsafe" >&2; exit 1; fi
done
STAGING="$(mktemp -d)"
trap 'rm -rf "$STAGING"' EXIT
git clone --depth 1 https://github.com/budagbogor/dailytrading.git "$STAGING/repo"
for part in app backend tests scripts .github; do
  mkdir -p "$STAGING/repo/$part"
  cp -R "$ROOT/$part/." "$STAGING/repo/$part/"
done
for part in README.md settings.gradle.kts build.gradle.kts .gitignore; do
  [[ ! -f "$ROOT/$part" ]] || cp "$ROOT/$part" "$STAGING/repo/$part"
done
cd "$STAGING/repo"
find . -type d -name __pycache__ -prune -exec rm -rf {} +
find . -type f -name '*.pyc' -delete
git add app backend tests scripts .github README.md settings.gradle.kts build.gradle.kts .gitignore
git diff --cached --check
if git diff --cached --quiet; then echo "Source already synchronized"; exit 0; fi
git commit -m "Sync complete QuantSyariah source tree"
git push origin HEAD:main
echo "Source pushed; check GitHub Actions for APK build result."
