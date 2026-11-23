"""List free photos of a mall on Wikimedia Commons.
Usage: python3 find_photo.py "Mall name city"
Prints candidates (title, size, licence, author, original URL, description). Only free licences are listed.
Pick an OUTSIDE view of the building, landscape or square, at least 1200 px wide."""
import json, re, sys, urllib.parse, urllib.request
UA = "MallsWorldwide/1.0 (https://projectshadowpages.github.io/malls-media/; projectshadowpages@gmail.com)"
q = urllib.parse.quote(sys.argv[1])
url = (f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={q}&gsrnamespace=6"
       f"&gsrlimit=20&prop=imageinfo&iiprop=url|extmetadata|size&format=json")
import time
d = None
for attempt in range(5):
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30)); break
    except Exception as e:
        print("retry:", e, file=sys.stderr); time.sleep(10 * (attempt + 1))
if d is None: sys.exit("Commons search failed - build without photo")
ok = ("CC0", "Public domain", "CC BY 2.0", "CC BY 3.0", "CC BY 4.0", "CC BY-SA 2.0", "CC BY-SA 3.0", "CC BY-SA 4.0", "CC BY-SA 2.5", "CC BY 2.5")
strip = lambda t: re.sub("<[^>]+>", "", t or "").strip()
for p in (d.get("query", {}).get("pages", {}) or {}).values():
    ii = p["imageinfo"][0]; md = ii.get("extmetadata", {})
    lic = strip(md.get("LicenseShortName", {}).get("value"))
    if not any(lic.startswith(o) for o in ok) or not p["title"].lower().endswith((".jpg", ".jpeg", ".png")):
        continue
    print(json.dumps({"title": p["title"], "w": ii["width"], "h": ii["height"], "licence": lic,
                      "author": strip(md.get("Artist", {}).get("value"))[:80],
                      "url": ii["url"], "desc": strip(md.get("ImageDescription", {}).get("value"))[:160]}, ensure_ascii=False))
