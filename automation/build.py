"""Build carousel JPEGs + reel (with music) for one mall.
Usage: python3 build.py mall.json
mall.json fields:
  date (YYYY-MM-DD), slug, name, city, country,
  flag (known name like "france" OR {"h":[[r,g,b],...]} / {"v":[[r,g,b],...]}),
  accent [r,g,b], icon (dome|circle|wave|box|fish|cart|gem|roof),
  slides: list of [kicker, headline, [body lines]] -> always 5 items (7 slides: cover/title + 5 + end)
  photo (optional): {"url": "https://upload.wikimedia.org/...jpg (original file URL)",
                     "credit": "Photo: <author> / Wikimedia Commons, <licence>"}
  cover (with photo): 2-4 short UPPERCASE headline lines, the key words line starts with "*" (yellow),
                     e.g. ["THE MALL WITH", "AN INDOOR", "*WAVE POOL"]. Photo becomes slide 1.
  caption (English), address (2 lines)
Output: ../media/<date>/<prefix>-01.jpg ... , <prefix>-reel.mp4, caption.txt
"""
import glob, json, os, subprocess, sys, time, urllib.parse, urllib.request
from PIL import Image, ImageFilter, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render

UA = "MallsWorldwide/1.0 (https://projectshadowpages.github.io/malls-media/; projectshadowpages@gmail.com)"

def fetch_commons(url, dest):
    """Download a Wikimedia Commons image as a standard-size thumbnail (1920px, fallback 960px)."""
    p = urllib.parse.urlparse(url)
    parts = p.path.split("/")  # /wikipedia/commons/a/ab/File.jpg
    if "thumb" not in parts:
        fname = parts[-1]; base = "/".join(parts[:-1]).replace("/commons/", "/commons/thumb/", 1)
    else:
        i = parts.index("thumb"); fname = parts[i + 3]; base = "/".join(parts[:i + 3])
    for w in (1920, 960):
        u = f"{p.scheme}://{p.netloc}{base}/{fname}/{w}px-{fname}"
        for attempt in range(3):
            try:
                req = urllib.request.Request(u, headers={"User-Agent": UA})
                data = urllib.request.urlopen(req, timeout=30).read()
                if data[:3] == b"\xff\xd8\xff" or data[:4] == b"\x89PNG":
                    open(dest, "wb").write(data); return True
            except Exception:
                pass
            try:  # fallback: curl (works better behind some proxies)
                subprocess.run(["curl", "-s", "-f", "-A", UA, "-o", dest, u], check=True, timeout=60)
                if open(dest, "rb").read(4)[:3] == b"\xff\xd8\xff": return True
            except Exception:
                pass
            time.sleep(3)
    return False

m = json.load(open(sys.argv[1]))
m["accent"] = tuple(m["accent"])
# Layout rotation (Lars 27.11.): a different carousel layout each day, cycle of 4; "layout" in the JSON overrides
ROTATE_LAYOUTS = True  # approved by Lars 27.11.
if "layout" not in m and ROTATE_LAYOUTS:
    import datetime as _dt
    m["layout"] = render.LAYOUTS[_dt.date.fromisoformat(m["date"]).toordinal() % len(render.LAYOUTS)]
m["slides"] = [(k, h, list(b)) for k, h, b in m["slides"]]
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
out = os.path.join(root, "media", m["date"]); os.makedirs(out, exist_ok=True)
prefix = m["slug"].lower()
tmp = f"/tmp/build_{prefix}"; os.makedirs(tmp, exist_ok=True)

photo = m.get("photo")
if photo and not fetch_commons(photo["url"], f"{tmp}/photo.jpg"):
    print("WARNING: photo download failed - building without photo slide"); photo = None
content = m["slides"][:5]
n = len(content) + 2
cover = m.get("cover")
if photo and cover:
    imgs = [render.cover_slide(m, n, f"{tmp}/photo.jpg", cover, photo.get("credit", ""))]
elif photo:  # old style: title slide + photo slide
    content = m["slides"][:4]; n = len(content) + 3
    imgs = [render.title_slide(m, n), render.photo_slide(m, 2, n, f"{tmp}/photo.jpg", photo.get("kicker", "THE BUILDING"), photo["line"], photo["credit"])]
else:
    imgs = [render.title_slide(m, n)]
start = len(imgs) + 1
imgs += [render.content_slide(m, start + i, n, *s) for i, s in enumerate(content)]
imgs.append(render.end_slide(m, n))
slides = []
for i, im in enumerate(imgs, 1):
    p = os.path.join(out, f"{prefix}-{i:02d}.jpg"); im.convert("RGB").save(p, quality=90); slides.append(p)
cap = m["caption"]
if photo and photo["credit"] not in cap:
    cap += "\n\n" + photo["credit"]
# TEST since 25.11.: no address block in the caption (IG carousels with it failed: "We restrict certain activity")
open(os.path.join(out, "caption.txt"), "w").write(cap + "\n")

# Story "New post" (9:16): blurred background, title slide in the middle, label on top
def new_post_story(label="NEW POST", sub=None, fname="story"):
    from PIL import ImageDraw
    SW, SH = 1080, 1920
    src = Image.open(slides[0]).convert("RGB")
    r = max(SW / src.width, SH / src.height); bg = src.resize((int(src.width * r) + 1, int(src.height * r) + 1))
    bg = bg.crop(((bg.width - SW) // 2, (bg.height - SH) // 2, (bg.width - SW) // 2 + SW, (bg.height - SH) // 2 + SH))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(40))).enhance(0.4)
    t = Image.open(slides[0]).convert("RGB"); tw = 820; t = t.resize((tw, int(t.height * tw / t.width)))
    y0 = (SH - t.height) // 2 + 40
    d = ImageDraw.Draw(bg)
    d.rectangle([(SW - tw) // 2 - 4, y0 - 4, (SW + tw) // 2 + 3, y0 + t.height + 3], outline=(255, 255, 255), width=4)
    bg.paste(t, ((SW - tw) // 2, y0))
    acc = tuple(m["accent"]); k = render.font("ExtraBold", 96); txt = label
    d.text(((SW - d.textlength(txt, font=k)) / 2, y0 - 190), txt, font=k, fill=acc)
    k2 = render.font("Medium", 44); txt2 = sub or f"{len(slides)} slides about {m['name']}"
    if d.textlength(txt2, font=k2) > SW - 120: txt2 = "30 seconds: today's mall" if sub else f"{len(slides)} slides: today's mall"
    d.text(((SW - d.textlength(txt2, font=k2)) / 2, y0 + t.height + 60), txt2, font=k2, fill=(255, 255, 255))
    k3 = render.font("Medium", 38); txt3 = "Tap our profile to see it"
    d.text(((SW - d.textlength(txt3, font=k3)) / 2, y0 + t.height + 130), txt3, font=k3, fill=(200, 200, 200))
    p = os.path.join(out, f"{prefix}-{fname}.jpg"); bg.save(p, quality=90); return p
story = new_post_story()
reel_story = new_post_story("NEW REEL", f"30 seconds: {m['name']}", "story-reel")

# Publication times vary a little per day (against "template" look): post 14:50-15:10, story +5 min, reel +60 min
off = int(m["date"].replace("-", "")) * 13 % 61 - 30  # post between 14:30 and 15:30 (Lars 26.11.)
def hm(mins): return f"{mins // 60:02d}:{mins % 60:02d}"
times = {"post": hm(900 + off), "story": hm(905 + off), "reel": hm(960 + off), "reel_story": hm(965 + off)}

def run(c): subprocess.run(c, check=True)

# Music: a licensed track from ../music (chosen by date), else a generated chord pad
# Durations (Lars 24.11.): first and last slide 3 s, content slides 5 s (time to read)
fade = 0.4
durs = [3.0] + [5.0] * (len(slides) - 2) + [3.0]
total = sum(durs) - (len(slides) - 1) * fade
tracks = sorted(glob.glob(os.path.join(root, "music", "*.mp3")) + glob.glob(os.path.join(root, "music", "*.m4a")))
music = f"{tmp}/music.m4a"
if tracks:
    tr = tracks[int(m["date"].replace("-", "")) % len(tracks)]
    run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-ss", "5", "-i", tr, "-t", str(total + 1), "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", music])
    music_name = os.path.basename(tr)
else:
    sets = [[(220, 261.63, 329.63), (174.61, 220, 261.63), (261.63, 329.63, 392), (196, 246.94, 293.66)],
            [(293.66, 349.23, 440), (233.08, 293.66, 349.23), (261.63, 329.63, 392), (220, 277.18, 329.63)],
            [(261.63, 329.63, 392), (220, 261.63, 329.63), (174.61, 220, 261.63), (196, 246.94, 293.66)],
            [(329.63, 392, 493.88), (261.63, 329.63, 392), (293.66, 349.23, 440), (246.94, 293.66, 369.99)]]
    ch = sets[int(m["date"][-2:]) % len(sets)]
    def note(k): return f"if(lt(mod(t,16),4),{ch[0][k]},if(lt(mod(t,16),8),{ch[1][k]},if(lt(mod(t,16),12),{ch[2][k]},{ch[3][k]})))"
    expr = "0.12*(" + "+".join(f"sin(2*PI*{note(k)}*t)" for k in range(3)) + ")*(0.6+0.4*sin(2*PI*0.5*t))"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"aevalsrc='{expr}|{expr}':s=48000:d=40",
         "-af", "lowpass=f=2000,aecho=0.6:0.5:250:0.3,afade=t=in:d=1.5", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", music])
    music_name = "generated"

# Reel frames: native 9:16, slide centred on a blurred, darkened copy of itself (no black bars)
RW, RH = 1080, 1920
frames = []
for i, p in enumerate(slides, 1):
    s = Image.open(p).convert("RGB")
    r = max(RW / s.width, RH / s.height); bg = s.resize((int(s.width * r) + 1, int(s.height * r) + 1))
    bg = bg.crop(((bg.width - RW) // 2, (bg.height - RH) // 2, (bg.width - RW) // 2 + RW, (bg.height - RH) // 2 + RH))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(40))).enhance(0.45)
    bg.paste(s, (0, (RH - s.height) // 2))
    f = f"{tmp}/r{i}.png"; bg.save(f); frames.append(f)
inputs = []
for f, dd in zip(frames, durs): inputs += ["-loop", "1", "-t", str(dd), "-i", f]
inputs += ["-i", music]; flt, last = "", "0:v"
for i in range(1, len(frames)):
    flt += f"[{last}][{i}:v]xfade=transition=fade:duration={fade}:offset={sum(durs[:i]) - i*fade:.2f}[v{i}];"; last = f"v{i}"
flt += f"[{last}]format=yuv420p[o];[{len(frames)}:a]atrim=0:{total:.2f},afade=t=in:d=0.5,afade=t=out:st={total-1.5:.2f}:d=1.5[a]"
run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", flt, "-map", "[o]", "-map", "[a]",
     "-r", "30", "-c:v", "libx264", "-profile:v", "high", "-preset", "veryfast", "-crf", "20", "-g", "60",
     "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", os.path.join(out, f"{prefix}-reel.mp4")])
print(json.dumps({"slides": [os.path.basename(s) for s in slides], "photo": bool(photo), "reel": f"{prefix}-reel.mp4",
                  "story": os.path.basename(story), "reel_story": os.path.basename(reel_story), "times": times,
                  "seconds": round(total, 1), "music": music_name}))
