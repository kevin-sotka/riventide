#!/usr/bin/env bash
# Build the browser (pygbag) version of Riventide into docs/ for GitHub Pages.
#
# Prereqs: tools/build_web_assets.py has been run at least once to produce
# web/assets (transcoded .ogg/.webp). That step is slow and idempotent, so it
# is NOT re-run here automatically.
#
# Usage:  bash tools/build_web.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
STAGE="$ROOT/build/pygbag_app"
OUT="$ROOT/docs"

if [ ! -d "$ROOT/web/assets" ]; then
  echo "ERROR: web/assets missing. Run: $PY tools/build_web_assets.py" >&2
  exit 1
fi

echo "==> staging app"
rm -rf "$STAGE"
mkdir -p "$STAGE"
cp "$ROOT/web_main.py" "$STAGE/main.py"
rsync -a --exclude='__pycache__' --exclude='.DS_Store' "$ROOT/game/" "$STAGE/game/"
mkdir -p "$STAGE/web"
rsync -a "$ROOT/web/assets/" "$STAGE/web/assets/"

echo "==> pygbag build"
# NOTE: the whole build/ dir must be removed, not just build/web. A leftover
# build/web-cache makes pygbag exit 0 while producing no output at all.
cd "$STAGE"
rm -rf build
"$PY" -m pygbag --build --width 800 --height 600 --ume_block 0 --app_name Riventide .

echo "==> publishing to docs/"
rm -rf "$OUT"
mkdir -p "$OUT"
cp "$STAGE/build/web/index.html" \
   "$STAGE/build/web/favicon.png" \
   "$STAGE/build/web/pygbag_app.apk" \
   "$STAGE/build/web/pygbag_app.tar.gz" "$OUT/"
touch "$OUT/.nojekyll"

# pygbag hardcodes a 16:9 framebuffer ratio regardless of --width/--height.
sed -i '' 's/fb_ar   :  1.77/fb_ar   :  1.333/' "$OUT/index.html"

# First load pulls down ~30MB (python + pygame + assets) with only a tiny
# progress sliver to show for it, so it reads as a hang rather than a wait -
# this is the same "blue screen" confusion that prompted the .webp fix above.
# Set expectations instead of leaving the default blank status text.
sed -i '' 's/id="status">Downloading\.\.\./id="status">Downloading Riventide (~60-90s first time)\.\.\. worth the wait/' "$OUT/index.html"
sed -i '' 's/id="infobox">Loading, please wait \.\.\./id="infobox">Loading Riventide... the wait is worth it/' "$OUT/index.html"

# pygbag's own show_infobox() centers #infobox by reading window.innerWidth
# at whatever instant custom_onload() happens to fire, which can be well
# before the page has laid out to its real size - it set the box to
# left:-66px/top:-49px (fully off-screen) in testing. Since that JS sets an
# inline style, only an !important stylesheet rule can override it; force
# true centering with CSS instead of trusting the JS math.
sed -i '' 's/position: fixed; \/\* center relative to viewport \*\//position: fixed !important; left: 50% !important; top: 50% !important; transform: translate(-50%, -50%) !important;/' "$OUT/index.html"

# GitHub Pages cannot resolve Git LFS objects; keep docs/ out of LFS.
cat > "$OUT/.gitattributes" <<'ATTR'
# GitHub Pages cannot resolve Git LFS objects - it serves the ~130-byte
# pointer file instead of the real asset, so the game would fail to load.
# The repo-root .gitattributes routes *.png (and .wav/.mp3/.mp4) through LFS,
# so unset those filters for everything in docs/: these must be plain blobs.
# Verify after a rebuild with:  git check-attr filter -- docs/pygbag_app.apk
* -filter -diff -merge
ATTR

echo "==> done. docs/ contents:"
ls -la "$OUT"
