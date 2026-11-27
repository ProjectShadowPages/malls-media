# Learnings and rules (status 27.11.2026) - also the template for every new Shadow Page

Read this together with RUN.md / RUN-news.md. German master copy: concept doc "Shadow Pages - Gesamtkonzept", section
"Erkenntnisse und Festlegungen 26./27.11." (Version 56).

## Instagram restriction ("We restrict certain activity")
- Metricool reports every IG carousel as "published with some warnings: Instagram restricted activity". The post IS live.
  Not caused by: first comment (arrives), address in caption, alt texts. Never repost.
- 26.11.: a manual "tag people" edit in the app was blocked with the same message -> account-level action limit.
- Until Lars lifts it (test 1.12.): NO carouselTags (see RUN.md), only mention a confirmed handle in the caption.
  Lars does no active actions (no comments elsewhere, no follows, no tagging, no post edits); only pins our first comment once.
- Rule for all SPs: when this message appears for an action, stop, never retry, pause active actions 5 days, then test once.

## Confirmed handles
- automation/mall-handles.md = handles confirmed by Lars in the app; treat as verified. GUM (Russia): do not tag.

## Trial reels and Instagram music (Metricool)
- instagramData.type "TRIAL_REEL" works (shareTrialAutomatically false).
- Instagram library music: instagramData.audioConfiguration {"audioId": "<numeric id>", "audioVolume": 100, "videoVolume": 0}.
  A text search term returns a candidate list -> retry with the numeric id. videoVolume 0 mutes our own Pixabay track.
  Whether the music survives publishing: see runlog (test 27.11. 18:31, Metricool 443125901).
- Never re-upload an already published reel as a trial reel (duplicate). Trial reels = new content, own formats for
  non-followers (then/now, guessing game), no "comment" call to action, one genuine question.
- Built: media/trial/duesseldorf-arcaden-trial.mp4 (scheduled 27.11.), media/trial/guess-malls-trial.mp4 (waiting for Lars).

## Settings (Instagram, done 26.11.)
- 2FA: SMS code never arrives; passkey (Google Password Manager) is enough. Contacts upload OFF, share to Facebook OFF,
  no public contact data, account suggestions ON, search engines ON, Kontostatus green. New recommended item: website embeds ON.
- Never crosspost to Lars' personal Facebook profile; the Facebook page gets everything via Metricool.

## Wikimedia downloads
- thumb.wikimedia.org is blocked by the proxy: use https://upload.wikimedia.org/wikipedia/commons/thumb/<a>/<ab>/<File>/1280px-<File>
- Commons API returns 429 often: retry with 20-30 s pauses, send a User-Agent with contact.

## Template for every new SP
1. Day 1: full settings checklist; passkey is fine; never sync contacts; never share to a private profile; no public contact data;
   account suggestions, search engines and website embeds ON.
2. Start slowly; on "We restrict certain activity" pause active actions for 5 days.
3. Every post: keyword alt texts, one genuine question, our own first comment (owner pins it), no engagement bait, hooks true.
4. Tag official accounts only if linked on the official website or confirmed by the owner (handle list per SP).
5. Trial reels only with new content.
6. Daily evening preview to the owner; short task list 50 min before the post.

## Carousel layouts
- Since 28.11.: 4 rotating layouts (classic, band, number, split) chosen by date in build.py; logo, flag, colours, fonts unchanged. Reason: the same template every day may cost reach (originality). Template for new SPs: build 3-4 layout variants from day one.

## Concept doc maintenance (Lars 27.11.)
- Every change to the concept doc: bump the version, set the "Stand" date at the top to today, AND check that the
  "Status (...)" line in "Kurzfassung" and the "Stand:" date of the To-Do list still match today; tick finished To-Do items.
