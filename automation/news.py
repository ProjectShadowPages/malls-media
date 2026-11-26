"""Build news story images (1080x1920 JPEG).
Usage: python3 news.py news-<date>.json
JSON: {"date":"YYYY-MM-DD","items":[{"slug":"thai-malls","accent":[r,g,b],"region":"THAILAND",
  "flag_file":"Flag_of_Thailand.svg"  (exact Wikimedia Commons file name of the country's flag; public domain),
  "headline":"...", "facts":[["600M baht","explanation"],...max 3], "source":"Outlet, 20 Nov 2026"}]}
Output: ../media/<date>/news-<slug>-story.jpg
"""
import json, os, sys, hashlib, subprocess, urllib.request
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

FLAGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flags"); os.makedirs(FLAGS, exist_ok=True)
UA = "malls-media/1.0 (projectshadowpages@gmail.com)"
def get_flag(fname, h=120):
    """Real flag from Wikimedia Commons (cached in automation/flags/). Returns an RGB image or None."""
    if not fname: return None
    cache = os.path.join(FLAGS, fname.replace(".svg", ".png"))
    if not os.path.exists(cache):
        md = hashlib.md5(fname.encode()).hexdigest()
        for w in (500, 330):  # Commons only serves standard thumbnail widths
            u = f"https://upload.wikimedia.org/wikipedia/commons/thumb/{md[0]}/{md[:2]}/{fname}/{w}px-{fname}.png"
            try:
                subprocess.run(["curl", "-s", "-f", "-L", "-A", UA, "-o", cache, u], check=True, timeout=60)
                if open(cache, "rb").read(4) == b"\x89PNG": break
            except Exception:
                pass
            if os.path.exists(cache): os.remove(cache)
        if not os.path.exists(cache): return None
    im = Image.open(cache).convert("RGBA"); bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    return bg.convert("RGB").resize((round(im.width * h / im.height), h))
files = []
for it in cfg["items"]:
    acc = tuple(it["accent"])
    s = Image.new("RGB", (W, H)); d = ImageDraw.Draw(s); d.rectangle([0, 0, W, 16], fill=acc)
    d.text((96, 120), "MALL NEWS", font=font("Bold", 44), fill=acc)
    r = it["region"].upper(); d.text((W - 96 - d.textlength(r, font=font("Medium", 36)), 126), r, font=font("Medium", 36), fill=WHITE)
    fl = get_flag(it.get("flag_file"))
    if fl:
        x0 = (W - fl.width) // 2; s.paste(fl, (x0, 250)); d.rectangle([x0 - 1, 249, x0 + fl.width, 250 + fl.height], outline=WHITE, width=2)
    elif it.get("flag_file"): print("WARNING: flag not found:", it["flag_file"], file=sys.stderr)
    y = center(d, 420, it["headline"], font("ExtraBold", 92)) + 70
    for big, small in it["facts"][:3]:
        y = center(d, y, big, font("ExtraBold", 90), fill=acc)
        y = center(d, y, small, font("Medium", 46), lh=1.25) + 40
    center(d, 1700, "Source: " + it["source"], font("Medium", 36))
    center(d, 1760, "@malls_oftheworld", font("Medium", 38))
    p = os.path.join(out, f"news-{it['slug']}-story.jpg"); s.save(p, quality=90); files.append(os.path.basename(p))
print(json.dumps(files))
