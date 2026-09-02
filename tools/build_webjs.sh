#!/usr/bin/env bash
# Assemble the browser (vanilla JS) build of Riventide into web-js/dist/.
#
# This is the replacement for the pygbag build in tools/build_web.sh. Where
# that one ships a 32MB archive containing CPython, pygame and every asset,
# this one ships a single HTML file plus a 195KB story graph and streams the
# images and audio on demand.
#
# Prereqs: tools/build_web_assets.py has been run at least once to produce
# web/assets (transcoded .jpg/.png/.ogg). That step is slow and idempotent,
# so it is NOT re-run here.
#
# Usage:  bash tools/build_webjs.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
SRC="$ROOT/web-js"
OUT="$SRC/dist"

if [ ! -d "$ROOT/web/assets" ]; then
  echo "ERROR: web/assets missing. Run: $PY tools/build_web_assets.py" >&2
  exit 1
fi

echo "==> extracting story graph from game/world/world.py"
"$PY" "$ROOT/tools/extract_story.py"

echo "==> assembling $OUT"
rm -rf "$OUT"
mkdir -p "$OUT"
cp "$SRC/index.html" "$SRC/story.json" "$OUT/"
rsync -a --exclude='.DS_Store' "$ROOT/web/assets/" "$OUT/assets/"
touch "$OUT/.nojekyll"

# GitHub Pages cannot resolve Git LFS objects; it serves the ~130-byte pointer
# instead of the real file. The repo-root .gitattributes routes *.png/*.jpg
# through LFS, so unset those filters for anything published from here.
cat > "$OUT/.gitattributes" <<'ATTR'
# Published assets must be plain blobs - GitHub Pages cannot resolve Git LFS.
* -filter -diff -merge
ATTR

echo "==> done"
du -sh "$OUT"
echo "    index.html  $(wc -c < "$OUT/index.html" | tr -d ' ') bytes"
echo "    story.json  $(wc -c < "$OUT/story.json" | tr -d ' ') bytes"
echo "    assets      $(find "$OUT/assets" -type f | wc -l | tr -d ' ') files"
echo
echo "To publish this instead of the pygbag build:"
echo "    rm -rf docs && cp -R $OUT docs"
