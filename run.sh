#!/bin/sh

python run.py \
    --roi-top 1156 \
    --roi-bottom 1868 \
    --roi-left 1400 \
    --roi-right 2502 \
    --h-padding 500 \
    --ratio 16 9 \
    one/* \
&& \
python run.py \
    --roi-top 1270 \
    --roi-bottom 1976 \
    --roi-left 1384 \
    --roi-right 2496 \
    --h-padding 500 \
    --ratio 16 9 \
    two/* \
&& \
ffmpeg -framerate 5 -pattern_type glob -i 'cropped/*.png' \
  -c:v libx264 -pix_fmt yuv420p out.mp4
