"""Build carousel JPEGs + reel (with generated music) for one mall.
Usage: python3 build.py mall.json
mall.json fields: date (YYYY-MM-DD), slug, name, city, country,
  flag (known name like "france" OR {"h":[[r,g,b],...]} / {"v":[[r,g,b],...]}),
  accent [r,g,b], icon (dome|circle|wave|box|fish|cart|gem|roof),
  slides: list of [kicker, headline, [body lines]]  (4-7 items -> 6-9 slides),
  caption (English, ends with hashtags), address (2 lines)
Output: ../media/<date>/<prefix>-01.jpg ... , <prefix>-reel.mp4, caption.txt
"""
import json, os, subprocess, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render

m = json.load(open(sys.argv[1]))
m["accent"] = tuple(m["accent"])
m["slides"] = [(k, h, list(b)) for k, h, b in m["slides"]]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, "media", m["date"]); os.makedirs(out, exist_ok=True)
prefix = m["slug"].lower()
n = len(m["slides"]) + 2
imgs = [render.title_slide(m, n)] + [render.content_slide(m, i + 2, n, *s) for i, s in enumerate(m["slides"])] + [render.end_slide(m, n)]
slides = []
for i, im in enumerate(imgs, 1):
    p = os.path.join(out, f"{prefix}-{i:02d}.jpg"); im.convert("RGB").save(p, quality=90); slides.append(p)
open(os.path.join(out, "caption.txt"), "w").write(m["caption"] + "\n\n\n" + m["address"] + "\n")

def run(c): subprocess.run(c, check=True)
tmp = f"/tmp/build_{prefix}"; os.makedirs(tmp, exist_ok=True)
sets = [[(220, 261.63, 329.63), (174.61, 220, 261.63), (261.63, 329.63, 392), (196, 246.94, 293.66)],
        [(293.66, 349.23, 440), (233.08, 293.66, 349.23), (261.63, 329.63, 392), (220, 277.18, 329.63)],
        [(261.63, 329.63, 392), (220, 261.63, 329.63), (174.61, 220, 261.63), (196, 246.94, 293.66)],
        [(329.63, 392, 493.88), (261.63, 329.63, 392), (293.66, 349.23, 440), (246.94, 293.66, 369.99)]]
ch = sets[int(m["date"][-2:]) % len(sets)]
def note(k): return f"if(lt(mod(t,16),4),{ch[0][k]},if(lt(mod(t,16),8),{ch[1][k]},if(lt(mod(t,16),12),{ch[2][k]},{ch[3][k]})))"
expr = "0.12*(" + "+".join(f"sin(2*PI*{note(k)}*t)" for k in range(3)) + ")*(0.6+0.4*sin(2*PI*0.5*t))"
music = f"{tmp}/music.m4a"
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"aevalsrc='{expr}|{expr}':s=48000:d=40",
     "-af", "lowpass=f=2000,aecho=0.6:0.5:250:0.3,afade=t=in:d=1.5", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", music])
W, H = 1080, 1920
frames = []
for i, p in enumerate(slides, 1):
    c = Image.new("RGB", (W, H)); c.paste(Image.open(p), (0, (H - 1350) // 2)); f = f"{tmp}/r{i}.png"; c.save(f); frames.append(f)
dur, fade = 3.2, 0.4
inputs = []
for f in frames: inputs += ["-loop", "1", "-t", str(dur), "-i", f]
inputs += ["-i", music]; flt, last = "", "0:v"
for i in range(1, len(frames)):
    flt += f"[{last}][{i}:v]xfade=transition=fade:duration={fade}:offset={i*(dur-fade):.2f}[v{i}];"; last = f"v{i}"
total = len(frames) * dur - (len(frames) - 1) * fade
flt += f"[{last}]format=yuv420p[o];[{len(frames)}:a]atrim=0:{total:.2f},afade=t=out:st={total-1.5:.2f}:d=1.5[a]"
run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", flt, "-map", "[o]", "-map", "[a]",
     "-r", "30", "-c:v", "libx264", "-profile:v", "high", "-preset", "veryfast", "-crf", "20", "-g", "60",
     "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", os.path.join(out, f"{prefix}-reel.mp4")])
print(json.dumps({"slides": [os.path.basename(s) for s in slides], "reel": f"{prefix}-reel.mp4", "seconds": round(total, 1)}))
