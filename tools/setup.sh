#!/usr/bin/env bash
# Reels editing environment setup: serif fonts + speech-to-text.
set -euo pipefail

FONT_DIR="$HOME/.fonts"
BASE="https://raw.githubusercontent.com/google/fonts/main/ofl"
mkdir -p "$FONT_DIR"
for p in \
  "playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf" \
  "playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf" \
  "instrumentserif/InstrumentSerif-Regular.ttf" \
  "instrumentserif/InstrumentSerif-Italic.ttf"; do
  name="$(basename "$p" | sed 's/%5B/[/; s/%5D/]/')"
  [ -f "$FONT_DIR/$name" ] || curl -sSL "$BASE/$p" -o "$FONT_DIR/$name"
done
fc-cache -f >/dev/null

pip install -q faster-whisper

echo "ffmpeg: $(ffmpeg -version | head -1)"
fc-list | grep -ciE "playfair|instrument|jetbrains" | xargs echo "fonts found:"
code=$(curl -s -o /dev/null -w '%{http_code}' https://huggingface.co || true)
echo "huggingface.co: HTTP $code (000 = blocked, Whisper model cannot download)"
