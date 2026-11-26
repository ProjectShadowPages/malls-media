"""Build a 9:16 news reel from the day's story images.
Usage: python3 news_reel.py <date> news-a-story.jpg news-b-story.jpg ...   (files in ../media/<date>/)
Output: ../media/<date>/news-reel.mp4 (5.5 s per story, music from ../music if present)"""
import glob, os, subprocess, sys
date, files = sys.argv[1], sys.argv[2:]
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
d = os.path.join(root, "media", date); frames = [os.path.join(d, f) for f in files]
dur, fade = 5.5, 0.4  # Lars 26.11.: 2 s longer per story, so the text can be read
total = len(frames) * dur - (len(frames) - 1) * fade
tracks = sorted(glob.glob(os.path.join(root, "music", "*.mp3")) + glob.glob(os.path.join(root, "music", "*.m4a")))
music = "/tmp/news_music.m4a"
def run(c): subprocess.run(c, check=True)
if tracks:
    tr = tracks[(int(date.replace("-", "")) + 7) % len(tracks)]
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "5", "-i", tr, "-t", str(total + 1), "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", music])
else:
    expr = "0.1*(sin(2*PI*220*t)+sin(2*PI*277.18*t)+sin(2*PI*329.63*t))*(0.6+0.4*sin(2*PI*0.5*t))"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"aevalsrc='{expr}|{expr}':s=48000:d=40",
         "-af", "lowpass=f=2000,aecho=0.6:0.5:250:0.3", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", music])
inputs = []
for f in frames: inputs += ["-loop", "1", "-t", str(dur), "-i", f]
inputs += ["-i", music]; flt, last = "", "0:v"
for i in range(1, len(frames)):
    flt += f"[{last}][{i}:v]xfade=transition=slideleft:duration={fade}:offset={i*(dur-fade):.2f}[v{i}];"; last = f"v{i}"
flt += f"[{last}]scale=1080:1920,format=yuv420p[o];[{len(frames)}:a]atrim=0:{total:.2f},afade=t=out:st={total-1.5:.2f}:d=1.5[a]"
run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", flt, "-map", "[o]", "-map", "[a]", "-r", "30",
     "-c:v", "libx264", "-profile:v", "high", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "128k",
     "-ar", "48000", "-ac", "2", "-movflags", "+faststart", os.path.join(d, "news-reel.mp4")])
print("news-reel.mp4", round(total, 1), "s")
