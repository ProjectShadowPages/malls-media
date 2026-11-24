# Daily news run – Malls Worldwide (@malls_oftheworld)

Goal: 4 mall-news STORIES (images) on Instagram + Facebook at 17:00, 18:00, 19:00 and 20:00 (Europe/Berlin) of the
target date. On WEDNESDAYS and SATURDAYS additionally ONE news REEL at 21:00 built from these 4 stories.
English. Nothing else: no posts, no likes/comments/follows.

0. Target date = date in the task prompt (normally today). Call Metricool getScheduledPosts for 16:30-21:30 that day.
   If non-draft stories for 17:00-20:00 already exist, stop and only log "already scheduled".
1. Repo ProjectShadowPages/malls-media (GitHub Pages: https://projectshadowpages.github.io/malls-media/).
2. Read automation/news-log.md. Do not repeat a news item listed there.
3. Search the web for shopping-mall news PUBLISHED in the last 4 days (check the article date; older articles are not
   allowed even if the event is recent), worldwide (openings, closures, sales of malls, big new stores, visitor/sales
   figures, holiday trading, records). Open each source page and take facts ONLY from it. Reliable outlets only
   (newspapers, trade press, company releases). Pick 4 different items, ideally from different countries/continents.
4. Write automation/news-<date>.json (format in automation/news.py docstring): 4 items, short headline (max ~40 chars),
   1-3 facts each with a big number/word + one short line, source = outlet + date. 4 different accent colours.
5. Run: cd automation && python3 news.py news-<date>.json   (pip install pillow --break-system-packages if missing)
6. Wednesday or Saturday only: python3 news_reel.py <date> <the 4 story file names in order>
7. Look at the images; nothing may overflow (source line must be one line).
   INDEPENDENT CHECK (before anything is pushed or scheduled): start a SEPARATE fresh sub-agent with the Agent tool
   (it must not have seen your work). Give it only: the image file paths, news-<date>.json (with the source URL of each item) and the source URLs. Its task:
   open every image and check (1) flag correct for the country (never looks like another country's flag),
   (2) every number/name/date matches the sources (open them), (3) spelling and grammar, (4) no text cut off,
   overlapping or overflowing, (5) each article is really from the last 4 days, (6) caption/headlines true, no clickbait.
   It answers "PASS" or a numbered list of errors. Fix every error, rebuild, and run the check again (max 2 rounds).
   If errors remain after 2 rounds: schedule nothing, log them in runlog.md. If no Agent tool exists, do the same
   checklist yourself very carefully, image by image. Write "check: PASS" (or the fixes) into runlog.md.
8. Append the 4 items to automation/news-log.md (date, headline, source URL). git add, commit, push to main.
9. Wait ~3 minutes until the files are online on GitHub Pages.
10. Metricool (blogId 8252854, Europe/Berlin), providers instagram + facebook, autoPublish true, draft false:
    - 4 stories, NO text: instagramData {"type":"STORY"}, facebookData {"type":"STORY"}, one image each,
      at 17:00, 18:00, 19:00, 20:00.
    - Wed/Sat: reel at 21:00: instagramData {"type":"REEL","showReelOnFeed":true}, facebookData {"type":"REEL","title":"Mall news"},
      text = "Mall news from around the world 🗞️" + one line per news item + a question + "#mallsoftheworld #mallnews #shopping #retailnews".
11. Append a result line to automation/runlog.md (date, "NEWS", headlines, reel yes/no, Metricool ids, OK/ERROR) and push.
If a step fails twice: schedule nothing, log the error, push.
