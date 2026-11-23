# News run – Malls Worldwide (@malls_oftheworld)

Goal: 3 mall-news STORIES (images only) on Instagram + Facebook. English. Nothing else: no posts, no reels, no likes/comments.

1. Repo ProjectShadowPages/malls-media (GitHub Pages: https://projectshadowpages.github.io/malls-media/).
2. Read automation/news-log.md. Do not repeat a news item listed there.
3. Search the web for shopping-mall news PUBLISHED in the last 4 days (check the article date; older articles are not allowed even if the event is recent), worldwide (openings, closures, sales of malls,
   big new stores, visitor/sales figures). Open each source page and take facts ONLY from it. Use reliable outlets
   (newspapers, trade press, company releases). Pick 3 different items, ideally from different countries.
4. Write automation/news-<date>.json (format in automation/news.py docstring): short headline (max ~40 chars),
   1-3 facts each with a big number/word + one short line, source = outlet + date. accent: pick 3 different colours.
5. Run: cd automation && python3 news.py news-<date>.json   (pip install pillow --break-system-packages if missing)
6. Look at the 3 images; nothing may overflow (source line must be one line).
7. Append the 3 items to automation/news-log.md (date, headline, source URL). git add, commit, push to main.
8. Wait ~3 minutes until the files are online on GitHub Pages.
9. Metricool (blogId 8252854, Europe/Berlin), providers instagram + facebook, autoPublish true, draft false, NO text:
   instagramData {"type":"STORY"}, facebookData {"type":"STORY"}, one image each, at the times given in the task (1 minute apart).
10. Append a result line to automation/runlog.md (date, "NEWS", 3 headlines, Metricool ids, OK/ERROR) and push.
If a step fails twice: schedule nothing, log the error, push.
