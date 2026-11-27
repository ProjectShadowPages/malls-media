import math, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))

W, H = 1080, 1350
M = 96
WHITE = (255, 255, 255)
BASE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(BASE, "fonts") + "/"
def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)

# ---------- flags ----------
def star(d, cx, cy, r, fill, rot=-90):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.4
        a = math.radians(rot + i * 36)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)

def flag(kind, w=300, h=200):
    im = Image.new("RGB", (w, h), WHITE); d = ImageDraw.Draw(im)
    if isinstance(kind, dict):
        cols = [tuple(c) for c in kind.get("h") or kind.get("v")]; n = len(cols)
        for i, c in enumerate(cols):
            if "h" in kind: d.rectangle([0, i*h/n, w, (i+1)*h/n], fill=c)
            else: d.rectangle([i*w/n, 0, (i+1)*w/n, h], fill=c)
        return im
    if kind == "italy":
        d.rectangle([0, 0, w/3, h], fill=(0, 146, 70)); d.rectangle([2*w/3, 0, w, h], fill=(206, 43, 55))
    elif kind in ("iceland", "denmark"):
        bg = (2, 82, 156) if kind == "iceland" else (200, 16, 46)
        d.rectangle([0, 0, w, h], fill=bg)
        cx = w * (7/18 if kind == "iceland" else 14/37)
        t = h * (4/18 if kind == "iceland" else 4/28)
        d.rectangle([cx - t/2, 0, cx + t/2, h], fill=WHITE); d.rectangle([0, h/2 - t/2, w, h/2 + t/2], fill=WHITE)
        if kind == "iceland":
            t2 = h * 2/18
            d.rectangle([cx - t2/2, 0, cx + t2/2, h], fill=(220, 30, 53)); d.rectangle([0, h/2 - t2/2, w, h/2 + t2/2], fill=(220, 30, 53))
    elif kind == "japan":
        r = h * 0.3; d.ellipse([w/2 - r, h/2 - r, w/2 + r, h/2 + r], fill=(188, 0, 45))
    elif kind == "pakistan":
        g = (1, 65, 28); d.rectangle([w/4, 0, w, h], fill=g)
        cx, cy = w * 0.625, h/2
        r1 = h * 0.30; d.ellipse([cx - r1, cy - r1, cx + r1, cy + r1], fill=WHITE)
        r2 = h * 0.27; ox, oy = cx + h*0.08, cy - h*0.06
        d.ellipse([ox - r2, oy - r2, ox + r2, oy + r2], fill=g)
        star(d, cx + h*0.17, cy - h*0.12, h*0.1, WHITE, rot=-50)
    elif kind == "nigeria":
        d.rectangle([0, 0, w/3, h], fill=(0, 135, 81)); d.rectangle([2*w/3, 0, w, h], fill=(0, 135, 81))
    elif kind == "thailand":
        d.rectangle([0, 0, w, h/6], fill=(165, 25, 49)); d.rectangle([0, 5*h/6, w, h], fill=(165, 25, 49))
        d.rectangle([0, 2*h/6, w, 4*h/6], fill=(45, 42, 74))
    elif kind == "russia":
        d.rectangle([0, h/3, w, 2*h/3], fill=(0, 57, 166)); d.rectangle([0, 2*h/3, w, h], fill=(213, 43, 30))
    elif kind == "kuwait":
        d.rectangle([0, 0, w, h/3], fill=(0, 122, 61)); d.rectangle([0, 2*h/3, w, h], fill=(206, 17, 38))
        d.polygon([(0, 0), (w/4, h/3), (w/4, 2*h/3), (0, h)], fill=(0, 0, 0))
    elif kind == "canada":
        red = (216, 6, 33)
        d.rectangle([0, 0, w/4, h], fill=red); d.rectangle([3*w/4, 0, w, h], fill=red)
        leaf = [(0,-1),(.13,-.75),(.27,-.8),(.2,-.38),(.45,-.62),(.5,-.5),(.75,-.55),(.65,-.3),(.75,-.25),
                (.4,.05),(.45,.2),(.05,.15),(.05,.6),(-.05,.6),(-.05,.15),(-.45,.2),(-.4,.05),(-.75,-.25),
                (-.65,-.3),(-.75,-.55),(-.5,-.5),(-.45,-.62),(-.2,-.38),(-.27,-.8),(-.13,-.75)]
        s = h * 0.36; cx, cy = w/2, h/2 + h*0.04
        d.polygon([(cx + x*s, cy + y*s) for x, y in leaf], fill=red)
    elif kind == "philippines":
        d.rectangle([0, 0, w, h/2], fill=(0, 56, 168)); d.rectangle([0, h/2, w, h], fill=(206, 17, 38))
        tw = h * math.sqrt(3) / 2; gold = (252, 209, 22)
        d.polygon([(0, 0), (tw, h/2), (0, h)], fill=WHITE)
        cx, cy = tw / 3, h / 2; r = h * 0.09
        for k in range(8):  # 8 rays (each a narrow triangle)
            a = math.radians(k * 45 + 22.5)
            for da in (-7, 0, 7):
                b = math.radians(k * 45 + 22.5 + da)
                d.polygon([(cx + r*0.9*math.cos(b - 0.12), cy + r*0.9*math.sin(b - 0.12)),
                           (cx + r*2.0*math.cos(b), cy + r*2.0*math.sin(b)),
                           (cx + r*0.9*math.cos(b + 0.12), cy + r*0.9*math.sin(b + 0.12))], fill=gold)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=gold)
        s = h * 0.055
        for sx, sy in ((h*0.08, h*0.09), (h*0.08, h*0.91), (tw - h*0.11, h/2)):
            star(d, sx, sy, s, gold)
    elif kind == "qatar":
        d.rectangle([0, 0, w, h], fill=(138, 21, 56))
        a, b = w * 0.25, w * 0.37; pts = [(0, 0), (a, 0)]
        for i in range(9):
            pts += [(b, (i + 0.5) * h / 9), (a, (i + 1) * h / 9)]
        pts += [(0, h)]; d.polygon(pts, fill=WHITE)
    elif kind == "poland":
        d.rectangle([0, h/2, w, h], fill=(220, 20, 60))
    elif kind == "usa":  # 13 stripes, blue canton (7 stripes high, 2/5 wide) with 50 stars (rows of 6 and 5)
        red, blue = (178, 34, 52), (60, 59, 110)
        for i in range(0, 13, 2): d.rectangle([0, i*h/13, w, (i+1)*h/13], fill=red)
        cw, ch = w * 0.4, h * 7 / 13; d.rectangle([0, 0, cw, ch], fill=blue)
        r = ch * 0.045
        for row in range(9):
            n = 6 if row % 2 == 0 else 5
            for col in range(n):
                x = cw * ((2*col + 1) / 12 if n == 6 else (2*col + 2) / 12)
                y = ch * (row + 1) / 10
                star(d, x, y, r, WHITE)
    return im

# ---------- icons (white line art in a box) ----------
def icon(d, kind, cx, cy, s, col):
    lw = max(6, s // 22)
    if kind == "dome":
        d.arc([cx - s/2, cy - s/2, cx + s/2, cy + s/2], 180, 360, fill=col, width=lw)
        for x in (-s/4, 0, s/4):
            d.line([cx + x, cy - (s/2 if x == 0 else s*0.43), cx + x, cy + s/3], fill=col, width=lw)
        d.line([cx - s/2, cy, cx + s/2, cy], fill=col, width=lw)
        d.line([cx - s/2, cy + s/3, cx + s/2, cy + s/3], fill=col, width=lw)
    elif kind == "circle":
        for k in (0.5, 0.33, 0.16):
            d.ellipse([cx - s*k, cy - s*k, cx + s*k, cy + s*k], outline=col, width=lw)
    elif kind == "wave":
        for row in (-s/5, s/10, s*0.4):
            pts = [(cx - s/2 + i, cy + row + math.sin(i / s * 4 * math.pi) * s/12) for i in range(0, int(s) + 1, 4)]
            d.line(pts, fill=col, width=lw)
    elif kind == "box":
        p = [(cx, cy - s/2), (cx + s/2, cy - s/4), (cx + s/2, cy + s/4), (cx, cy + s/2), (cx - s/2, cy + s/4), (cx - s/2, cy - s/4)]
        d.line(p + [p[0]], fill=col, width=lw, joint="curve")
        d.line([(cx - s/2, cy - s/4), (cx, cy), (cx + s/2, cy - s/4)], fill=col, width=lw)
        d.line([(cx, cy), (cx, cy + s/2)], fill=col, width=lw)
    elif kind == "fish":
        d.ellipse([cx - s/2, cy - s/4, cx + s/5, cy + s/4], outline=col, width=lw)
        d.polygon([(cx + s/6, cy), (cx + s/2, cy - s/4), (cx + s/2, cy + s/4)], outline=col, width=lw)
        r = s/22; d.ellipse([cx - s/3 - r, cy - s/12 - r, cx - s/3 + r, cy - s/12 + r], fill=col)
    elif kind == "cart":
        d.line([(cx - s/2, cy - s/2.5), (cx - s/3, cy - s/2.5), (cx - s/5, cy + s/6), (cx + s/2.4, cy + s/6), (cx + s/2, cy - s/4), (cx - s/3.4, cy - s/4)], fill=col, width=lw, joint="curve")
        for x in (-s/8, s/3):
            r = s/12; d.ellipse([cx + x - r, cy + s/3 - r, cx + x + r, cy + s/3 + r], outline=col, width=lw)
    elif kind == "gem":
        p=[(cx-s/2,cy-s/6),(cx-s/4,cy-s/2.4),(cx+s/4,cy-s/2.4),(cx+s/2,cy-s/6),(cx,cy+s/2)]
        d.line(p+[p[0]],fill=col,width=lw,joint="curve")
        d.line([(cx-s/2,cy-s/6),(cx+s/2,cy-s/6)],fill=col,width=lw)
        d.line([(cx-s/4,cy-s/2.4),(cx-s/8,cy-s/6),(cx,cy+s/2),(cx+s/8,cy-s/6),(cx+s/4,cy-s/2.4)],fill=col,width=max(3,lw//2))
    elif kind == "roof":
        for k in range(3):
            y = cy - s/4 + k * s/4
            pts = [(cx - s/2 + i, y - math.sin(i / s * math.pi) * s/5) for i in range(0, int(s) + 1, 4)]
            d.line(pts, fill=col, width=lw)
        for x in (-s/4, 0, s/4):
            d.line([cx + x, cy - s/2.3, cx + x, cy + s/2.5], fill=col, width=max(3, lw//2))

# ---------- text helpers ----------
def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines

def footer(d, i, n, accent):
    f = font("Medium", 30)
    d.text((M, H - 100), "@malls_oftheworld", font=f, fill=WHITE)
    t = f"{i}/{n}"; d.text((W - M - d.textlength(t, font=f), H - 100), t, font=f, fill=WHITE)
    d.rectangle([0, 0, W, 14], fill=accent)

def title_slide(m, n):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(BASE, "logo.png")).convert("RGB").resize((200, 200))
    im.paste(logo, (M - 36, 40))
    fw, fh = 195, 130
    fl = flag(m["flag"], fw, fh); im.paste(fl, ((W - fw)//2, 240))
    d.rectangle([(W - fw)//2 - 2, 238, (W + fw)//2 + 1, 240 + fh + 1], outline=WHITE, width=2)
    k = font("ExtraBold", 60); t = "MALL OF THE DAY"
    d.text(((W - d.textlength(t, font=k))/2, 420), t, font=k, fill=m["accent"])
    icon(d, m["icon"], W/2, 640, 170, WHITE)
    size = 104
    while True:
        f = font("ExtraBold", size); lines = wrap(d, m["name"], f, W - 2*M)
        if len(lines) <= 3 and all(d.textlength(l, font=f) <= W - 2*M for l in lines): break
        size -= 4
    y = 800
    for l in lines:
        d.text(((W - d.textlength(l, font=f))/2, y), l, font=f, fill=WHITE); y += int(size * 1.12)
    y += 20; d.rectangle([W/2 - 90, y, W/2 + 90, y + 8], fill=m["accent"]); y += 40
    f2 = font("SemiBold", 52); t = f"{m['city']}, {m['country']}"
    d.text(((W - d.textlength(t, font=f2))/2, y), t, font=f2, fill=WHITE)
    footer(d, 1, n, m["accent"]); return im

def photo_slide(m, idx, n, photo, kicker, line, credit):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    ph = Image.open(photo).convert("RGB"); ah = 880
    r = max(W / ph.width, ah / ph.height); ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1))
    x0 = (ph.width - W) // 2; y0 = (ph.height - ah) // 2
    im.paste(ph.crop((x0, y0, x0 + W, y0 + ah)), (0, 0))
    d.rectangle([0, ah, W, ah + 10], fill=m["accent"])
    y = ah + 50
    d.text((M, y), kicker, font=font("Bold", 38), fill=m["accent"]); y += 70
    for l in wrap(d, line, font("ExtraBold", 64), W - 2*M)[:3]:
        d.text((M, y), l, font=font("ExtraBold", 64), fill=WHITE); y += 76
    cf = font("Medium", 24)
    cl = wrap(d, credit, cf, W - 2*M)[:2]
    cy = H - 150 - 30 * (len(cl) - 1)
    for l in cl:
        d.text((M, cy), l, font=cf, fill=(170, 170, 170)); cy += 30
    footer(d, idx, n, m["accent"]); return im

def cover_slide(m, n, photo, lines, credit):
    if m.get("layout") in ("band", "split"):
        return cover_top(m, n, photo, lines, credit)
    return cover_classic(m, n, photo, lines, credit)

def cover_classic(m, n, photo, lines, credit):
    """Photo cover: full-bleed photo, dark gradient, big headline (line starting with * = yellow)."""
    im = Image.open(photo).convert("RGB")
    r = max(W / im.width, H / im.height); im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1))
    x0 = (im.width - W) // 2; y0 = max(0, (im.height - H) // 3)
    im = im.crop((x0, y0, x0 + W, y0 + H))
    black = Image.new("RGB", (W, H), (0, 0, 0))
    g = Image.new("L", (1, H))
    for y in range(H): g.putpixel((0, y), int(240 * min(1, max(0, (y - H * 0.30) / (H * 0.45)))))
    im = Image.composite(black, im, g.resize((W, H)))
    t = Image.new("L", (1, H))
    for y in range(H): t.putpixel((0, y), int(150 * max(0, 1 - y / 260)))
    im = Image.composite(black, im, t.resize((W, H)))
    logo = Image.open(os.path.join(BASE, "logo.png")).convert("RGB").resize((220, 220))
    mk = Image.new("L", (220, 220), 0); ImageDraw.Draw(mk).ellipse((0, 0, 219, 219), fill=255)
    im.paste(logo, (45, 35), mk)
    fl = flag(m["flag"], 180, 120); im.paste(fl, (W - 225, 85))
    d = ImageDraw.Draw(im); YEL = (255, 214, 0)
    clean = [l.lstrip("*") for l in lines][:4]
    size = 112
    while size > 60 and max(d.textlength(l, font=font("ExtraBold", size)) for l in clean) > W - 132: size -= 4
    f = font("ExtraBold", size); lh = int(size * 1.09)
    sub = f"{m['name']} \u00b7 {m['city']}, {m['country']}"; sf = font("Medium", 40)
    while d.textlength(sub, font=sf) > W - 140: sub = f"{m['name']} \u00b7 {m['country']}"; break
    y_end = H - 150 - (30 if credit else 0)
    y = y_end - 70 - lh * len(clean)
    d.text((70, y - 60), "MALL OF THE DAY", font=font("ExtraBold", 40), fill=m["accent"])
    for raw, l in zip(lines, clean):
        d.text((66, y), l, font=f, fill=YEL if raw.startswith("*") else WHITE); y += lh
    d.text((70, y + 16), sub, font=sf, fill=(230, 230, 230))
    if credit:
        d.text((70, H - 118), credit, font=font("Medium", 22), fill=(170, 170, 170))
    d.text((70, H - 76), "@malls_oftheworld", font=font("Medium", 28), fill=(200, 200, 200))
    s = font("ExtraBold", 34); t = "SWIPE  \u2192"
    d.text((W - 70 - d.textlength(t, font=s), H - 80), t, font=s, fill=WHITE)
    return im

def content_slide(m, idx, n, kicker, head, body):
    v = m.get("layout", "classic")
    if v != "classic" and VARIANTS.get(v):
        return VARIANTS[v](m, idx, n, kicker, head, body)
    return content_classic(m, idx, n, kicker, head, body)

def content_classic(m, idx, n, kicker, head, body):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    fl = flag(m["flag"], 138, 92); im.paste(fl, (W - M - 138, 86))
    d.rectangle([W - M - 139, 85, W - M, 178], outline=WHITE, width=1)
    d.text((M, 108), kicker, font=font("Bold", 38), fill=m["accent"])
    y = 260; hf = font("ExtraBold", 80)
    for l in wrap(d, head, hf, W - 2*M):
        d.text((M, y), l, font=hf, fill=WHITE); y += 94
    y += 24; d.rectangle([M, y, M + 140, y + 9], fill=m["accent"]); y += 70
    bf = font("Medium", 48); bullet = len(body) > 1
    bullet = len([p for p in body if not p.rstrip().endswith("\u2192")]) > 1
    for para in body:
        if para.rstrip().endswith("\u2192"):  # teaser line (Lars 25.11.): no bullet, accent colour
            tf = font("Bold", 46); y += 10
            for l in wrap(d, para, tf, W - 2*M):
                d.text((M, y), l, font=tf, fill=m["accent"]); y += 62
            continue
        lines = wrap(d, para, bf, W - 2*M - (50 if bullet else 0))
        for j, l in enumerate(lines):
            if bullet and j == 0:
                d.ellipse([M, y + 24, M + 16, y + 40], fill=m["accent"])
            d.text((M + (50 if bullet else 0), y), l, font=bf, fill=WHITE); y += 66
        y += 30
    footer(d, idx, n, m["accent"]); return im

def end_slide(m, n):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(BASE, "logo.png")).convert("RGB").resize((420, 420))
    im.paste(logo, ((W - 420)//2, 170))
    f = font("ExtraBold", 72); y = 680
    for l in ["A new mall", "every day."]:
        d.text(((W - d.textlength(l, font=f))/2, y), l, font=f, fill=WHITE); y += 86
    y += 30; d.rectangle([W/2 - 90, y, W/2 + 90, y + 8], fill=m["accent"]); y += 50
    f2 = font("SemiBold", 44)
    for l in ["Follow @malls_oftheworld", "Would you visit?"]:
        d.text(((W - d.textlength(l, font=f2))/2, y), l, font=f2, fill=WHITE); y += 66
    footer(d, n, n, m["accent"]); return im



# ---------- layout variants (Lars 27.11.: no identical template every day) ----------
# Rotated by date in build.py: classic, band, number, split. Logo, flag, colours and fonts stay the same.
import re as _re
YEL = (255, 214, 0)

def _body(d, body, y, x, maxw, accent, size=48):
    bf = font("Medium", size)
    bullet = len([p for p in body if not p.rstrip().endswith("\u2192")]) > 1
    for para in body:
        if para.rstrip().endswith("\u2192"):
            tf = font("Bold", size - 2); y += 10
            for l in wrap(d, para, tf, maxw):
                d.text((x, y), l, font=tf, fill=accent); y += int(size * 1.3)
            continue
        for j, l in enumerate(wrap(d, para, bf, maxw - (50 if bullet else 0))):
            if bullet and j == 0: d.ellipse([x, y + 24, x + 16, y + 40], fill=accent)
            d.text((x + (50 if bullet else 0), y), l, font=bf, fill=WHITE); y += int(size * 1.375)
        y += 30
    return y

def content_band(m, idx, n, kicker, head, body):
    """Accent band at the top with the kicker, headline below, body text."""
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    acc = m["accent"]; d.rectangle([0, 0, W, 200], fill=acc)
    dark = (0, 0, 0) if sum(acc) > 380 else WHITE
    d.text((M, 78), kicker, font=font("ExtraBold", 44), fill=dark)
    fl = flag(m["flag"], 120, 80); im.paste(fl, (W - M - 120, 60))
    d.rectangle([W - M - 121, 59, W - M, 140], outline=dark, width=2)
    y = 270; hf = font("ExtraBold", 76)
    for l in wrap(d, head, hf, W - 2*M):
        d.text((M, y), l, font=hf, fill=WHITE); y += 90
    y += 50
    _body(d, body, y, M, W - 2*M, acc)
    f = font("Medium", 30); d.text((M, H - 100), "@malls_oftheworld", font=f, fill=WHITE)
    t = f"{idx}/{n}"; d.text((W - M - d.textlength(t, font=f), H - 100), t, font=f, fill=WHITE)
    return im

def content_number(m, idx, n, kicker, head, body):
    """If the headline contains a number, show it huge (key-figure slide); otherwise centred layout."""
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im); acc = m["accent"]
    fl = flag(m["flag"], 138, 92); im.paste(fl, (W - M - 138, 86))
    d.rectangle([W - M - 139, 85, W - M, 178], outline=WHITE, width=1)
    d.text((M, 108), kicker, font=font("Bold", 38), fill=acc)
    rx = r"\d[\d,.]*\d(?:[\s-]*(?:m\u00b2|%|km|sq ft|million|billion|feet|acres?))?|\d+[\s-]*(?:m\u00b2|%|km|sq ft|million|billion|feet|acres?)"
    mt = _re.search(rx, head)
    src = head if mt else None
    if not mt:
        for para in body:
            mt = _re.search(rx, para)
            if mt and not para.rstrip().endswith("\u2192"): src = para; break
            mt = None
    y = 250
    if mt:
        num = mt.group(0).strip(); size = 220
        while size > 110 and d.textlength(num, font=font("ExtraBold", size)) > W - 2*M: size -= 10
        d.text((M - 6, y), num, font=font("ExtraBold", size), fill=acc); y += int(size * 1.12)
        hf = font("ExtraBold", 60)
        for l in wrap(d, head, hf, W - 2*M)[:3]:
            d.text((M, y), l, font=hf, fill=WHITE); y += 72
    else:
        hf = font("ExtraBold", 84)
        for l in wrap(d, head, hf, W - 2*M):
            d.text((M, y), l, font=hf, fill=WHITE); y += 98
    y += 40; d.rectangle([M, y, W - M, y + 3], fill=(70, 70, 70)); y += 50
    _body(d, body, y, M, W - 2*M, acc, 46)
    footer(d, idx, n, acc); return im

def content_split(m, idx, n, kicker, head, body):
    """Vertical accent bar on the left, text block indented, big slide number as watermark."""
    im = Image.new("RGB", (W, H), (12, 12, 12)); d = ImageDraw.Draw(im); acc = m["accent"]
    d.rectangle([0, 0, 28, H], fill=acc)
    bigf = font("ExtraBold", 420); t = f"{idx:02d}"
    d.text((W - 40 - d.textlength(t, font=bigf), H - 560), t, font=bigf, fill=(32, 32, 32))
    x = M + 30; mw = W - x - M
    fl = flag(m["flag"], 120, 80); im.paste(fl, (x, 90)); d.rectangle([x - 1, 89, x + 120, 170], outline=WHITE, width=1)
    d.text((x + 150, 110), kicker, font=font("Bold", 38), fill=acc)
    y = 250; hf = font("ExtraBold", 78)
    for l in wrap(d, head, hf, mw):
        d.text((x, y), l, font=hf, fill=WHITE); y += 92
    y += 50
    _body(d, body, y, x, mw, acc)
    f = font("Medium", 30); d.text((x, H - 100), "@malls_oftheworld", font=f, fill=WHITE)
    return im

def cover_top(m, n, photo, lines, credit):
    """Photo cover with the headline at the TOP (dark gradient from top), logo + flag at the bottom."""
    im = Image.open(photo).convert("RGB")
    r = max(W / im.width, H / im.height); im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1))
    x0 = (im.width - W) // 2; y0 = max(0, (im.height - H) // 2)
    im = im.crop((x0, y0, x0 + W, y0 + H)); black = Image.new("RGB", (W, H), (0, 0, 0))
    g = Image.new("L", (1, H))
    for y in range(H): g.putpixel((0, y), int(235 * min(1, max(0, (H * 0.62 - y) / (H * 0.42)))))
    im = Image.composite(black, im, g.resize((W, H)))
    b = Image.new("L", (1, H))
    for y in range(H): b.putpixel((0, y), int(200 * max(0, (y - (H - 300)) / 300)))
    im = Image.composite(black, im, b.resize((W, H)))
    d = ImageDraw.Draw(im)
    clean = [l.lstrip("*") for l in lines][:4]; size = 108
    while size > 60 and max(d.textlength(l, font=font("ExtraBold", size)) for l in clean) > W - 132: size -= 4
    f = font("ExtraBold", size); lh = int(size * 1.09); y = 110
    d.text((70, y), "MALL OF THE DAY", font=font("ExtraBold", 40), fill=m["accent"]); y += 70
    for raw, l in zip(lines, clean):
        d.text((66, y), l, font=f, fill=YEL if raw.startswith("*") else WHITE); y += lh
    sub = f"{m['name']} \u00b7 {m['city']}, {m['country']}"; sf = font("Medium", 40)
    if d.textlength(sub, font=sf) > W - 140: sub = f"{m['name']} \u00b7 {m['country']}"
    d.text((70, y + 16), sub, font=sf, fill=(230, 230, 230))
    logo = Image.open(os.path.join(BASE, "logo.png")).convert("RGB").resize((200, 200))
    mk = Image.new("L", (200, 200), 0); ImageDraw.Draw(mk).ellipse((0, 0, 199, 199), fill=255)
    im.paste(logo, (55, H - 260), mk)
    fl = flag(m["flag"], 150, 100); im.paste(fl, (285, H - 210))
    if credit: d.text((470, H - 150), credit[:60], font=font("Medium", 22), fill=(190, 190, 190))
    s = font("ExtraBold", 34); t = "SWIPE  \u2192"
    d.text((W - 70 - d.textlength(t, font=s), H - 90), t, font=s, fill=WHITE)
    return im

VARIANTS = {"band": content_band, "number": content_number, "split": content_split}
LAYOUTS = ["classic", "band", "number", "split"]
