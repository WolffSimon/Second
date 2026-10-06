#!/usr/bin/env bash
# Zip each skill folder on its own into dist/, ready to upload to Claude.ai (Customize > Skills).
# Usage: bash scripts/build_dist.sh
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$here/dist"
rm -f "$here/dist"/*.zip
cd "$here/skills"
for dir in */; do
  name="${dir%/}"
  zip -qr "$here/dist/$name.zip" "$name" -x "*/__pycache__/*" "*.DS_Store"
  echo "dist/$name.zip"
done
