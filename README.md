# bahar-academic-lab-assets
Images for Bahar Academic Lab Instagram posts.

- `posts/<NN-slug>/NN.png` — carousel slides (1080x1350), served via raw.githubusercontent.com for Metricool.
- `tools/build.py` + `tools/content.py` — renders carousels from `content.py` (needs Playwright + Chrome):
  `python3 tools/build.py <output_dir> [carousel-key ...]`
  Brand colors: cream #FEFAEE, brown #3C3026, coral #E65356, gold #C99C58. Font: Vazirmatn.
- `reels/<key>/reel.mp4` — silent faceless text reels (1080x1920, ~20 s), built by `python3 -I tools/reels.py <out_dir> [key ...]`; scenes/captions live in `tools/reels.py`.
