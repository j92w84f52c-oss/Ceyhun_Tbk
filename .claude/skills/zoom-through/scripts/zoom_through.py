#!/usr/bin/env python3
"""Render an "infinite zoom" MP4 that flies through a sequence of images.

Each image is nested in the centre of the one before it, scaled down by
--zoom. The camera zooms in at a constant rate, so every image grows until it
fills the frame and the next one is already waiting in its centre.
"""
import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def collect_images(inputs):
    paths = []
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            paths += sorted(f for f in p.iterdir() if f.suffix.lower() in IMAGE_EXTS)
        else:
            paths.append(p)
    return paths


def load(path, width, height, max_scale):
    """Cover-crop to the frame's aspect ratio, at up to max_scale x frame size."""
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    aspect = width / height
    w, h = img.size
    if w / h > aspect:
        nw = round(h * aspect)
        img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = round(w / aspect)
        img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    target_w = min(img.width, round(width * max_scale))
    target_w = max(target_w, width)
    return img.resize((target_w, round(target_w / aspect)), Image.LANCZOS)


def feather_mask(size, frac):
    """White rectangle whose edges fade to black over `frac` of the short side."""
    w, h = size
    border = max(1, round(min(w, h) * frac))
    mask = Image.new("L", (w, h), 0)
    mask.paste(255, (border, border, w - border, h - border))
    return mask.filter(ImageFilter.GaussianBlur(border / 2))


def draw_layer(frame, img, mask, scale):
    """Draw img centred on frame at `scale` x frame size (mask=None: opaque)."""
    W, H = frame.size
    if scale >= 1:
        cw, ch = img.width / scale, img.height / scale
        box = ((img.width - cw) / 2, (img.height - ch) / 2,
               (img.width + cw) / 2, (img.height + ch) / 2)
        layer = img.resize((W, H), Image.BILINEAR, box=box)
        m = None if mask is None else mask.resize((W, H), Image.BILINEAR, box=box)
        frame.paste(layer, (0, 0), m)
    else:
        dw, dh = round(W * scale), round(H * scale)
        if dw < 2 or dh < 2:
            return
        layer = img.resize((dw, dh), Image.BILINEAR)
        m = None if mask is None else mask.resize((dw, dh), Image.BILINEAR)
        frame.paste(layer, ((W - dw) // 2, (H - dh) // 2), m)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", help="image files and/or folders, outermost first")
    ap.add_argument("-o", "--output", default="zoom_through.mp4")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--seconds-per-image", type=float, default=3.0)
    ap.add_argument("--zoom", type=float, default=4.0,
                    help="how much smaller each image is than the previous one")
    ap.add_argument("--feather", type=float, default=0.12,
                    help="edge blend width as a fraction of the image's short side")
    ap.add_argument("--hold", type=float, default=1.0,
                    help="seconds to hold on the first and last image")
    ap.add_argument("--reverse", action="store_true", help="zoom out instead of in")
    args = ap.parse_args()

    paths = collect_images(args.inputs)
    if len(paths) < 2:
        sys.exit("need at least two images")
    W, H = args.width, args.height
    imgs = [load(p, W, H, args.zoom) for p in paths]
    masks = [None] + [feather_mask(i.size, args.feather) for i in imgs[1:]]

    def render(seg, t):
        """Frame at progress t in [0, 1] through the zoom from image seg to seg+1."""
        frame = Image.new("RGB", (W, H))
        zoom = args.zoom ** t
        for k in range(seg, len(imgs)):
            scale = zoom / args.zoom ** (k - seg)
            if W * scale < 2:
                break
            draw_layer(frame, imgs[k], masks[k] if k > seg else None, scale)
        return frame

    steps = max(1, round(args.seconds_per_image * args.fps))
    hold = round(args.hold * args.fps)
    times = [(0, 0.0)] * hold
    times += [(s, i / steps) for s in range(len(imgs) - 1) for i in range(steps)]
    times += [(len(imgs) - 1, 0.0)] * (hold + 1)
    if args.reverse:
        times.reverse()

    ffmpeg = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(args.fps), "-i", "-",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
         "-movflags", "+faststart", args.output],
        stdin=subprocess.PIPE)
    last = None
    for n, key in enumerate(times):
        if key != last:
            data = render(*key).tobytes()
            last = key
        ffmpeg.stdin.write(data)
        if n % args.fps == 0:
            print(f"\rframe {n + 1}/{len(times)}", end="", file=sys.stderr)
    ffmpeg.stdin.close()
    if ffmpeg.wait() != 0:
        sys.exit("ffmpeg failed")
    print(f"\nwrote {args.output} ({len(times) / args.fps:.1f}s, {len(imgs)} images)",
          file=sys.stderr)


if __name__ == "__main__":
    main()
