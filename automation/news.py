"""Build news story images (1080x1920 JPEG).
Usage: python3 news.py news-<date>.json
JSON: {"date":"YYYY-MM-DD","items":[{"slug":"thai-malls","accent":[r,g,b],"region":"THAILAND",
  "headline":"...", "facts":[["600M baht","explanation"],...max 3], "source":"Outlet, 20 Nov 2026"}]}
Output: ../media/<date>/news-<slug>-story.jpg
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import render
from render import font, WHITE
W, H = 1080, 1920
cfg = json.load(open(sys.argv[1]))
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, "media", cfg["date"]); os.makedirs(out, exist_ok=True)
def center(d, y, t, f, fill=WHITE, lh=1.15):
    for l in render.wrap(d, t, f, W - 192):
        d.text(((W - d.textlength(l, font=f)) / 2, y), l, font=f, fill=fill); y += int(f.size * lh)
    return y
files = []
for it in cfg["items"]:
    acc = tuple(it["accent"])
    s = Image.new("RGB", (W, H)); d = ImageDraw.Draw(s); d.rectangle([0, 0, W, 16], fill=acc)
    d.text((96, 120), "MALL NEWS", font=font("Bold", 44), fill=acc)
    r = it["region"].upper(); d.text((W - 96 - d.textlength(r, font=font("Medium", 36)), 126), r, font=font("Medium", 36), fill=WHITE)
    y = center(d, 420, it["headline"], font("ExtraBold", 92)) + 70
    for big, small in it["facts"][:3]:
        y = center(d, y, big, font("ExtraBold", 90), fill=acc)
        y = center(d, y, small, font("Medium", 46), lh=1.25) + 40
    center(d, 1700, "Source: " + it["source"], font("Medium", 36))
    center(d, 1760, "@malls_oftheworld", font("Medium", 38))
    p = os.path.join(out, f"news-{it['slug']}-story.jpg"); s.save(p, quality=90); files.append(os.path.basename(p))
print(json.dumps(files))
