#!/bin/bash
# usage: shot.sh <chapitre> <page> [sortie.png]   — capture d'une page d'un chapitre (Chromium sans écran)
B=$(ls -d ~/.cache/ms-playwright/chromium-1243/chrome-linux*/ | head -1)
OUT=${3:-/home/toto/ia-test/$1-$2.png}
timeout 100 $B/chrome --headless=new --no-sandbox --disable-gpu --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist --window-size=1400,820 --virtual-time-budget=${T:-12000} --enable-logging=stderr --v=0 --screenshot=$OUT "http://127.0.0.1:${PORT:-8002}/$1/index.html#$2" 2>&1 | grep -E "CONSOLE" | grep -viE "GPU stall|GL Driver|ReadPixels" | cut -c1-260 | head -6
echo "→ $OUT"
