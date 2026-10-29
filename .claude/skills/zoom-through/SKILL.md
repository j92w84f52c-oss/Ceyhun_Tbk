---
name: zoom-through
description: Render an "infinite zoom" MP4 that flies through a sequence of images, each one nested in the centre of the previous. Use when the user runs /zoom-through or asks for a zoom-through / infinite-zoom video from images.
---

# zoom-through

Turns an ordered list of images into a video where the camera zooms steadily
into the centre of each image and lands on the next one, which was nested
there all along.

## Steps

1. Find the images. Use what the user names; otherwise look for image files in
   the repo (ask if none are found or the order is unclear). The order is the
   zoom order: first image = outermost.
2. Run the script (needs `ffmpeg` and Pillow):

   ```bash
   python3 .claude/skills/zoom-through/scripts/zoom_through.py IMG_OR_DIR... -o out.mp4
   ```

   Options:
   - `--width/--height` (default 1280x720), `--fps` (30)
   - `--seconds-per-image` (3.0): duration of each zoom step
   - `--zoom` (4.0): how many times smaller each nested image is; higher = faster, more dramatic
   - `--feather` (0.12): soft edge width blending each image into the one around it
   - `--hold` (1.0): seconds to pause on the first and last image
   - `--reverse`: zoom out instead of in

   Images are centre-cropped to the frame's aspect ratio. Folder inputs are
   sorted by filename.
3. Tell the user where the video is and send it to them. Mention that images
   whose centre matches the next image's overall colours blend most seamlessly.
