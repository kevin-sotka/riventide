#!/usr/bin/env python3
"""
tools/build_web_assets.py

Repeatable asset transcoding pipeline for the pygame -> pygbag (web) port of
Riventide. Shrinks the desktop asset set down to something a browser can
reasonably download.

    assets/audio/**/*.wav    -> web/assets/audio/**/*.ogg          (Ogg Vorbis, ~96kbps, stereo)
    assets/graphics/**/*.png -> web/assets/graphics/**/*.jpg|.png (JPEG q85 for opaque images,
                                                                    PNG for images that need alpha)

Rules:
  - The original `assets/` tree is NEVER read-write touched. This script only
    ever opens files under `assets/` for reading. All output goes under `web/`.
  - Idempotent: a source file is skipped if its output already exists, is
    non-empty, and is newer than the source (mtime compare). Pass --force to
    re-transcode everything regardless.
  - Parallel: uses a ThreadPoolExecutor (default 6 workers, override with
    --workers). Both ffmpeg (external process) and Pillow (releases the GIL
    for its C encode/decode work) parallelize fine under threads.

Tooling note (discovered while building this):
  Images were originally transcoded to WebP via Pillow. That worked fine at
  build time, but the pygame-ce wasm build pygbag loads in-browser has no
  WebP decoder (its SDL2_image isn't compiled with libwebp), so every .webp
  image failed to load in the actual browser build with "Unsupported image
  format" - discovered only by running the deployed build, not by the build
  script itself. Switched to JPEG (quality 85) for the ~99% of source images
  that are fully opaque (AI-generated backgrounds/portraits with no alpha
  channel) and PNG for the handful that need one - both are baseline
  SDL2_image formats guaranteed present in any wasm build. See
  game/assets_config.py:graphics_path() for the per-file extension probe
  this requires on the loader side.

  The ffmpeg 8.1.2 build on this machine (`brew install ffmpeg`, the plain
  formula, not ffmpeg-full) has NO libwebp support at all -- `ffmpeg -codecs
  | grep webp` reports decode-only ("D.VILS webp"), and there's no cwebp
  binary either. So images are transcoded with Pillow (PIL) instead, which on
  this machine (python3 / Pillow 11.3.0) has JPEG/PNG encoding built in.
  Audio still goes through ffmpeg, using its native "vorbis" encoder (this
  build has no libvorbis either) -- confirmed via `ffmpeg -encoders`. The
  native encoder does not honor -b:a/-minrate/-maxrate (it silently produces
  a fixed quality regardless of requested bitrate), so bitrate is controlled
  with the native encoder's quality scale (`-q:a 2`, empirically ~90-95kbps
  stereo, closest available match to the ~96kbps target).

Usage:
    python3 tools/build_web_assets.py [--workers N] [--audio-only] [--graphics-only] [--force]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_AUDIO = ROOT / "assets" / "audio"
SRC_GRAPHICS = ROOT / "assets" / "graphics"
DST_AUDIO = ROOT / "web" / "assets" / "audio"
DST_GRAPHICS = ROOT / "web" / "assets" / "graphics"

FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"

AUDIO_VORBIS_QUALITY = "2"  # native ffmpeg vorbis encoder quality scale (~90-95kbps stereo)
IMAGE_JPEG_QUALITY = 85


def human(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}GB"


def needs_build(src: Path, dst: Path, force: bool) -> bool:
    if force:
        return True
    if not dst.exists():
        return True
    if dst.stat().st_size == 0:
        return True
    return src.stat().st_mtime > dst.stat().st_mtime


def transcode_audio(src: Path, dst: Path) -> tuple[bool, str]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    # ffmpeg picks its output muxer from the filename extension, so the temp
    # file must still end in .ogg (not .ogg.tmp) or format detection fails.
    tmp = dst.parent / f"{dst.stem}.tmp{dst.suffix}"
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-i", str(src),
        "-c:a", "vorbis", "-strict", "-2",
        "-q:a", AUDIO_VORBIS_QUALITY,
        "-ac", "2",
        str(tmp),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except Exception as e:  # noqa: BLE001
        tmp.unlink(missing_ok=True)
        return False, f"{src.name}: ffmpeg exec failed: {e}"
    if result.returncode != 0 or not tmp.exists() or tmp.stat().st_size == 0:
        tmp.unlink(missing_ok=True)
        return False, f"{src.name}: ffmpeg failed: {result.stderr.strip()[:300]}"
    tmp.replace(dst)
    return True, ""


def image_has_alpha(im) -> bool:
    return im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)


def transcode_image(src: Path, dst: Path) -> tuple[bool, str]:
    try:
        from PIL import Image
    except ImportError:
        return False, f"{src.name}: Pillow (PIL) not importable for {sys.executable}"

    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.parent / f"{dst.stem}.tmp{dst.suffix}"
    try:
        with Image.open(src) as im:
            # dst.suffix was already chosen (in collect_graphics_jobs) based
            # on whether this source image has alpha - .png for alpha,
            # .jpg (no alpha channel support) otherwise.
            if dst.suffix == ".png":
                if im.mode != "RGBA":
                    im = im.convert("RGBA")
                im.save(tmp, "PNG", optimize=True)
            else:
                if im.mode != "RGB":
                    im = im.convert("RGB")
                im.save(tmp, "JPEG", quality=IMAGE_JPEG_QUALITY, optimize=True)
    except Exception as e:  # noqa: BLE001
        tmp.unlink(missing_ok=True)
        return False, f"{src.name}: Pillow failed: {e}"
    if not tmp.exists() or tmp.stat().st_size == 0:
        tmp.unlink(missing_ok=True)
        return False, f"{src.name}: produced empty output"
    tmp.replace(dst)
    return True, ""


def collect_jobs(src_root: Path, dst_root: Path, pattern: str, new_suffix: str, force: bool):
    jobs = []
    skipped = 0
    for src in sorted(src_root.rglob(pattern)):
        if not src.is_file():
            continue
        rel = src.relative_to(src_root)
        dst = dst_root / rel.with_suffix(new_suffix)
        if needs_build(src, dst, force):
            jobs.append((src, dst))
        else:
            skipped += 1
    return jobs, skipped


def collect_graphics_jobs(src_root: Path, dst_root: Path, force: bool):
    """Like collect_jobs, but the output extension is decided per-file:
    .png for images with an alpha channel, .jpg (smaller, no alpha) for
    everything else. Also removes any stale sibling from a previous format
    (e.g. a leftover .webp, or a .jpg when the source has since gained
    alpha) so the web tree never ends up serving two versions of one image.
    """
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow (PIL) not importable, cannot inspect graphics for alpha", file=sys.stderr)
        raise SystemExit(1)

    jobs = []
    skipped = 0
    for src in sorted(src_root.rglob("*.png")):
        if not src.is_file():
            continue
        rel = src.relative_to(src_root)
        try:
            with Image.open(src) as im:
                alpha = image_has_alpha(im)
        except Exception:
            alpha = False
        chosen_ext = ".png" if alpha else ".jpg"
        stale_ext = ".jpg" if alpha else ".png"

        dst = dst_root / rel.with_suffix(chosen_ext)
        stale = dst_root / rel.with_suffix(stale_ext)
        stale.unlink(missing_ok=True)
        (dst_root / rel.with_suffix(".webp")).unlink(missing_ok=True)

        if needs_build(src, dst, force):
            jobs.append((src, dst))
        else:
            skipped += 1
    return jobs, skipped


def run_category(name: str, jobs, worker_fn, workers: int):
    results = []
    failures = []
    if not jobs:
        return results, failures
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        future_map = {pool.submit(worker_fn, src, dst): (src, dst) for src, dst in jobs}
        done = 0
        for fut in concurrent.futures.as_completed(future_map):
            src, dst = future_map[fut]
            done += 1
            ok, err = fut.result()
            if ok:
                results.append((src, dst))
            else:
                failures.append(err)
            print(f"  [{name}] {done}/{len(jobs)} {'OK' if ok else 'FAIL'}: {src.relative_to(ROOT)}"
                  + ("" if ok else f"  -- {err}"))
    return results, failures


def dir_size(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def main():
    ap = argparse.ArgumentParser(description="Transcode Riventide assets for the web (pygbag) build.")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--audio-only", action="store_true")
    ap.add_argument("--graphics-only", action="store_true")
    ap.add_argument("--force", action="store_true", help="Re-transcode even if output looks up to date.")
    args = ap.parse_args()

    do_audio = not args.graphics_only
    do_graphics = not args.audio_only

    print(f"Riventide web asset build")
    print(f"  root:   {ROOT}")
    print(f"  ffmpeg: {FFMPEG}")
    print(f"  python: {sys.executable}")
    print()

    all_failures = []
    t0 = time.time()

    src_audio_before = dir_size(SRC_AUDIO)
    src_gfx_before = dir_size(SRC_GRAPHICS)

    if do_audio:
        jobs, skipped = collect_jobs(SRC_AUDIO, DST_AUDIO, "*.wav", ".ogg", args.force)
        print(f"Audio: {len(jobs)} to transcode, {skipped} up to date (skipped)")
        _, fails = run_category("audio", jobs, transcode_audio, args.workers)
        all_failures += fails
        print()

    if do_graphics:
        jobs, skipped = collect_graphics_jobs(SRC_GRAPHICS, DST_GRAPHICS, args.force)
        print(f"Graphics: {len(jobs)} to transcode, {skipped} up to date (skipped)")
        _, fails = run_category("graphics", jobs, transcode_image, args.workers)
        all_failures += fails
        print()

    elapsed = time.time() - t0

    dst_audio_after = dir_size(DST_AUDIO)
    dst_gfx_after = dir_size(DST_GRAPHICS)

    print("=" * 60)
    print("SIZE REPORT")
    print("=" * 60)
    if do_audio:
        print(f"Audio:    {human(src_audio_before):>10}  ->  {human(dst_audio_after):>10}"
              f"  ({(1 - dst_audio_after / src_audio_before) * 100:.1f}% smaller)"
              if src_audio_before else "Audio: (no source files)")
    if do_graphics:
        print(f"Graphics: {human(src_gfx_before):>10}  ->  {human(dst_gfx_after):>10}"
              f"  ({(1 - dst_gfx_after / src_gfx_before) * 100:.1f}% smaller)"
              if src_gfx_before else "Graphics: (no source files)")

    total_web = dir_size(ROOT / "web")
    total_src = src_audio_before + src_gfx_before
    print("-" * 60)
    print(f"web/ total: {human(total_web)}   (source total considered: {human(total_src)})")
    print(f"Elapsed: {elapsed:.1f}s")

    if all_failures:
        print()
        print(f"FAILURES ({len(all_failures)}):")
        for f in all_failures:
            print(f"  - {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
