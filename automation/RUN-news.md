# Daily news run – Malls Worldwide (@malls_oftheworld)

**FIRST read automation/ig-mode.md (Instagram MODE: PAUSED / SLOW / NORMAL) and follow it - it overrides every Instagram step below.**


Read automation/LEARNINGS.md first (current restrictions and rules).

Goal: 4 mall-news STORIES (images) on Instagram + Facebook one every 6 hours: 03:00, 09:00, 15:00 and 21:00 (Europe/Berlin) of the
target date (Lars 24.11.: reach all time zones). On WEDNESDAYS and SATURDAYS additionally ONE news REEL at 21:30 built from
these 4 stories (or the best recent ones).
English. Nothing else: no posts, no likes/comments/follows.

0. Target date = date in the task prompt (normally today). Call Metricool getScheduledPosts for 02:30-22:00 that day.
   If non-draft news stories for 03:00/09:00/15:00/21:00 already exist, stop and only log "already scheduled".
1. Repo ProjectShadowPages/malls-media (GitHub Pages: https://projectshadowpages.github.io/malls-media/).
2. Read automation/news-log.md. Do not repeat a news item listed there.
3. Search the web for shopping-mall news PUBLISHED in the last 4 days (check the article date; older articles are not
   allowed even if the event is recent), worldwide (openings, closures, sales of malls, big new stores, visitor/sales
   figures, holiday trading, records). Open each source page and take facts ONLY from it. Reliable outlets only
   (newspapers, trade press, company releases). Pick 4 different items, ideally from different countries/continents.
4. Write automation/news-<date>.json (format in automation/news.py docstring): 4 items, short headline (max ~40 chars),
   1-3 facts each with a big number/word + one short line, source = outlet + date. 4 different accent colours.
   Each item gets "flag_file": the exact Wikimedia Commons file name of the flag of the country the news is from
   (e.g. "Flag_of_the_United_States.svg", "Flag_of_Germany.svg", "Flag_of_Canada_(Pantone).svg"). news.py downloads it
   (cache: automation/flags/). If it prints "WARNING: flag not found", fix the file name and run again. Check every
   story image: the flag must be the right country.
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
      at 03:00, 09:00, 15:00, 21:00 (if a time is already in the past when you run, skip only that slot).
    - Wed/Sat: reel at 21:30: instagramData {"type":"REEL","showReelOnFeed":true}, facebookData {"type":"REEL","title":"Mall news"},
      text = "Mall news from around the world 🗞️" + one line per news item + a question + "#mallsoftheworld #mallnews #shopping #retailnews".
    - Wed/Sat also the SAME news reel as a YouTube Short at 21:40 (Lars 26.11.): provider youtube, youtubeData
      {"title":"Mall news: <most interesting headline> #shorts" (max 100 chars),"type":"short","privacy":"public",
      "tags":["mall news","shopping malls","retail news","malls of the world"],"category":"TRAVEL_EVENTS","madeForKids":false,"isAiGeneratedContent":false}, text = one line per news item (with source names)
      + a genuine question + "#mallnews #shopping #shorts".
11. Append a result line to automation/runlog.md (date, "NEWS", headlines, reel yes/no, Metricool ids, OK/ERROR) and push.
If a step fails twice: schedule nothing, log the error, push.
