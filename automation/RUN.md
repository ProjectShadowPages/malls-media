# Daily mall run – Malls Worldwide (@malls_oftheworld)

Goal: create ONE mall carousel (7 slides) + ONE "new post" story + ONE reel for the target date and schedule them in Metricool.
Times vary a little each day (build.py prints them under "times": post 14:50-15:10, story +5 min, reel +60 min). Everything in English.
Never post anything else. Never like, follow or comment.

## Steps
0. Target date = the date given in the task prompt (normally tomorrow, Europe/Berlin).
   First call Metricool getScheduledPosts (blogId 8252854, Europe/Berlin) for the target date 14:00-17:00.
   If a non-draft POST or REEL between 14:00 and 17:00 already exists, do NOT create new ones: log "already scheduled" and stop.
1. Repo is ProjectShadowPages/malls-media (public, GitHub Pages: https://projectshadowpages.github.io/malls-media/).
2. Read automation/malls-list.json. Pick a famous or interesting shopping mall/arcade that is NOT in the list
   (compare name and city). Vary countries/continents and types (historic arcade, mega mall, outlet, luxury, quirky).
   Read automation/viral-ideas.md first: about every second day pick a mall lead or use a pattern from it
   (absurd attraction, size in human terms, weird detail ...). Remove a used lead from that file.
3. Research it on the web. Use only facts you found in at least one reliable source (Wikipedia, official site,
   major newspaper). No guessing. Keep numbers exact as in the source.
4. COVER PHOTO (slide 1, approved by Lars 24.11.): the most striking photo of the mall - the famous attraction,
   the spectacular interior or the iconic outside view (whatever makes people stop scrolling):
   cd automation && python3 find_photo.py "<mall name> <city>"   (try also "<mall name> interior", "<attraction> <mall name>")
   Choose ONE candidate: sharp, bright, width >= 1200, clearly this mall (judge by title/description), no close-up
   faces of identifiable people. Only the free licences the script lists (CC0, public domain, CC BY, CC BY-SA); prefer CC0/PD.
   credit = "Photo: <author> / Wikimedia Commons, <licence>". If nothing suitable: no photo (then the black title slide is used).
5. Write automation/mall-<date>.json (format: see docstring in automation/build.py). Rules:
   - Always 7 slides: slide 1 (photo cover, or black title slide without photo) + 5 content slides + end slide.
   - cover: 2-4 short UPPERCASE lines that form the hook (true, no clickbait, max ~14 characters per line),
     the line with the key words starts with "*" (shown in yellow), e.g. ["THE MALL WITH", "AN INDOOR", "*WAVE POOL"].
     It should match the winning hook (see HOOKS) and the photo.
   - First content slide "QUICK FACTS" with 3-4 short bullet facts. Others: one surprising fact/story each.
   - Headlines max ~35 characters, body short (max ~180 characters per slide).
   - accent: vary it day by day (gold, teal, coral, violet, sky blue, lime ... never the same as yesterday).
   - flag: a known name (italy, iceland, denmark, japan, pakistan, nigeria, thailand, russia, kuwait, poland, france)
     or simple stripes {"h":[[r,g,b],...]} / {"v":[[r,g,b],...]}. Known names also: canada.
     Stripes only if the real flag is ONLY stripes. If the flag has an emblem (leaf, star, sun, crest ...),
     add it as a new named flag in render.py, render it and check the image: a flag must never look like
     another country's flag.
   - caption (vary the writing style every day: sometimes a question first, sometimes a number, sometimes a short story):
     line 1 = hook WITH search keywords, e.g. "The shopping mall in Bangkok you can reach by boat 🇹🇭";
     2-3 short sentences; a question with 👇 OR (about every second day) a share prompt like "Send this to the friend you would go with 👇"; then "#mallsoftheworld" plus 3-4 hashtags that fit THIS mall
     (city, country, special feature). Never repeat the same block. No banned or unrelated hashtags.
     If a photo is used, its credit line goes at the end of the caption (build.py adds it automatically).
     Write like a real person, short and natural: no filler words, no hype clichés ("nestled", "vibrant",
     "a must-visit", "whether you're…"), no long dashes, max ~60 words before the hashtags.
   - sources: list of the URLs you took the facts from (needed for the check in step 7).
   - address: "<Name>\n<street, postcode city, country>".
   - HOOKS: before writing caption line 1, write 10 different hooks (each under 12 words; curiosity, bold claim
     or surprising number; each must be true). Rank them, take the best for caption line 1 and the reel caption,
     the second best as headline of the most surprising slide. Keep search keywords (mall, city) in line 1.
     Write the winning hook into runlog.md.
   - Instagram handle of the mall: look for the official Instagram link on the mall's OFFICIAL website (footer/contact).
     Only if it is clearly linked there: mention it once in the caption ("📍 @handle") and tag it on slide 1
     (instagramData.carouselTags {"0":[{"username":"handle","x":0.5,"y":0.5}]}). Never guess a handle.
     If Metricool rejects the tag, schedule again without carouselTags but keep the mention. Write the handle (or "none") to runlog.md.
6. Run: cd automation && python3 build.py mall-<date>.json   (needs Pillow + ffmpeg; install if missing:
   pip install pillow --break-system-packages; apt-get install -y ffmpeg if needed).
   build.py downloads the photo, builds 7 slides and a 9:16 reel (first and last slide 3 s, content slides 5 s, about 29 s, music from /music).
7. Look at the slides (open slide 1 and 2 more JPEGs) to check that no text overflows, the cover headline is readable on the photo and the photo shows this mall.
   INDEPENDENT CHECK (before anything is pushed or scheduled): start a SEPARATE fresh sub-agent with the Agent tool
   (it must not have seen your work). Give it only: the image file paths, mall-<date>.json + caption.txt and the source URLs. Its task:
   open every image and check (1) flag correct for the country (never looks like another country's flag),
   (2) every number/name/date matches the sources (open them), (3) spelling and grammar, (4) no text cut off,
   overlapping or overflowing, (5) photo shows the right place, credit present, (6) caption/headlines true, no clickbait.
   It answers "PASS" or a numbered list of errors. Fix every error, rebuild, and run the check again (max 2 rounds).
   If errors remain after 2 rounds: schedule nothing, log them in runlog.md. If no Agent tool exists, do the same
   checklist yourself very carefully, image by image. Write "check: PASS" (or the fixes) into runlog.md.
8. Append the mall to automation/malls-list.json. git add, commit, push to main.
9. Wait until https://projectshadowpages.github.io/malls-media/media/<date>/<prefix>-01.jpg is online
   (about 1-3 min; Metricool fails if the file is not there yet). If you cannot check it directly, wait 3 minutes.
10. Metricool (blogId 8252854, timezone Europe/Berlin), providers instagram + facebook, autoPublish true, draft false:
   - times.post on target date: instagramData {"type":"POST"}, facebookData {"type":"POST"}, media = the 7 JPEG URLs,
     mediaAltText: TEST since 25.11. (Lars approved): send NO mediaAltText for this instagram/facebook carousel
     (empty list) - we check if the warning "We restrict certain activity" disappears. Keep alt texts on the other platforms.
     text = caption.txt content.
   - times.story: instagramData {"type":"STORY"}, facebookData {"type":"STORY"}, media = <prefix>-story.jpg URL, NO text.
   - times.reel_story: instagramData {"type":"STORY"}, facebookData {"type":"STORY"}, media = <prefix>-story-reel.jpg URL, NO text.
   - times.reel on target date: instagramData {"type":"REEL","showReelOnFeed":true}, facebookData {"type":"REEL","title":"<short title>"},
     media = reel URL, text = short caption (keyword hook line + question + same hashtags).
   Extra platforms (tested OK 24.11.), each a SEPARATE scheduled post with its own text (never copy the IG caption 1:1):
   - post + 20 min, provider threads, threadsData {}: media = the 7 JPEG URLs, text = hook line + 2 short sentences
     + question + exactly ONE topic hashtag (e.g. #shopping) + photo credit line. No hashtag block.
   - post + 25 min, provider bluesky, blueskyData {"postLanguages":["en"]}: media = max 4 JPEGs (slide 1 + the 3 most
     interesting), text max 300 characters INCLUDING the credit line (count it!), 1 hashtag.
   - post + 30 min, provider pinterest: media = slide 1 only, pinterestData {"boardId":"Shopping Malls of the World",
     "pinTitle":"<Mall>, <Country>: <hook> (max 100 chars)", "pinLink":"https://www.instagram.com/malls_oftheworld/",
     "pinNewFormat":false,"isAiGenerated":false}, text = SEO description 2-3 sentences with search words
     (shopping mall, city, country, travel) + 3 hashtags + credit if photo.
   - reel + 10 min, provider youtube: media = reel URL, youtubeData {"title":"<Mall>: <hook> #shorts" (max 100 chars),
     "type":"short","privacy":"public","tags":[mall, city, country, "shopping mall", "malls of the world"],
     "category":"TRAVEL_EVENTS","madeForKids":false,"isAiGeneratedContent":false}, text = 2-3 sentences + question
     + credit + "#shoppingmall #<city> #shorts".
   If one extra platform fails, still schedule the others and log the error.
11. Write a result line to automation/runlog.md (date, mall, photo yes/no, handle, music, times, Metricool ids of post/story/reel/threads/bluesky/pinterest/youtube, OK/ERROR) and push.
If any step fails: try once more. If it still fails, schedule nothing, write the error to runlog.md and push.

## Platforms
instagram + facebook (post, story, reel), threads, bluesky, pinterest, youtube (shorts) - all connected and tested 24.11.
Do not add other providers (no X, no TikTok, no LinkedIn) on your own.
