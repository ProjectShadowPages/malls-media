# Daily run – Malls Worldwide (@malls_oftheworld)

Goal: create ONE mall carousel + ONE reel for the target date and schedule both in Metricool. Everything in English.
No news, no stories (paused). Never post anything else. Never like or comment.

## Steps
0. Target date = the date given in the task prompt (normally tomorrow, Europe/Berlin).
   First call Metricool getScheduledPosts (blogId 8252854, Europe/Berlin) for the target date 14:00-17:00.
   If a non-draft POST or REEL for 15:00/16:00 already exists, do NOT create new ones: log "already scheduled" and stop.
1. Repo is ProjectShadowPages/malls-media (public, GitHub Pages: https://projectshadowpages.github.io/malls-media/).
2. Read automation/malls-list.json. Pick a famous or interesting shopping mall/arcade that is NOT in the list
   (compare name and city). Vary countries/continents.
3. Research it on the web. Use only facts you found in at least one reliable source (Wikipedia, official site,
   major newspaper). No guessing. Keep numbers exact as in the source.
4. Write automation/mall-<date>.json (format: see docstring in automation/build.py). Rules:
   - 4 content slides (= 6 slides in total). Slide 1 "QUICK FACTS" with 3-4 short bullet facts.
   - Headlines max ~35 characters, body short (max ~180 characters per slide).
   - flag: use a known name (italy, iceland, denmark, japan, pakistan, nigeria, thailand, russia, kuwait, poland, france)
     or simple stripes {"h":[[r,g,b],...]} / {"v":[[r,g,b],...]}. Prefer a mall whose country flag is simple stripes or listed.
   - caption: hook line with flag emoji, 2-3 short sentences, a question with 👇, then "#mallsoftheworld" plus 3-4 hashtags that fit THIS mall (city, country, special feature such as #artdeco, #rooftop, #aquarium). Vary them every day; never repeat the same block. No banned or unrelated hashtags. address: "<Name>\n<street, postcode city, country>".
5. Run: cd automation && python3 build.py mall-<date>.json   (needs Pillow + ffmpeg; install if missing:
   pip install pillow --break-system-packages; apt-get install -y ffmpeg if needed)
6. Look at the slides (open 2-3 JPEGs) to check that no text overflows.
7. Append the mall to automation/malls-list.json. git add, commit, push to main.
8. Wait until https://projectshadowpages.github.io/malls-media/media/<date>/<prefix>-01.jpg is online
   (about 1-3 min; Metricool fails if the file is not there yet). If you cannot check it directly, wait 3 minutes.
9. Metricool (blogId 8252854, timezone Europe/Berlin), providers instagram + facebook, autoPublish true, draft false:
   - 15:00 on target date: instagramData {"type":"POST"}, facebookData {"type":"POST"}, media = the 6 JPEG URLs,
     mediaAltText one short line per slide, text = caption + "\n\n\n" + address.
   - 16:00 on target date: instagramData {"type":"REEL","showReelOnFeed":true}, facebookData {"type":"REEL","title":"<short title>"},
     media = reel URL, text = short caption (1 line + question + same hashtags).
10. Write a result line to automation/runlog.md (date, mall, Metricool post ids, OK/ERROR) and push.
If any step fails: try once more. If it still fails, schedule nothing, write the error to runlog.md and push.

## Platforms
Currently only instagram + facebook. Threads, Pinterest, YouTube and Bluesky are added here only after they are
connected in Metricool and tested once (see Gesamtkonzept). Do not add other providers on your own.
