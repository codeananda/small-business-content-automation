---
name: daily-carousels
description: Write the day's Instagram carousels from new spoken ideas, sales call transcripts and WhatsApp chats, in the owner's brand voice, render the cards and save each post to a dated folder in Google Drive for review. Use when someone says "/daily-carousels", "make today's carousels", "Karussells für heute", or on the daily scheduled start. Never publishes anything.
---

# Daily carousels

Each run turns the newest raw material into 5 to 10 finished carousels (cards, caption and a short brief) in `<content_folder>/Carousels/<YYYY-MM-DD>/`, ready for a human to review, approve and post. It never posts.

**Scheduled runs ask nothing.** When this starts from a schedule, make every call yourself and stop only for a real blocker. Write the blocker into `<content_folder>/Carousels/<date>/SETUP NEEDED.md` and into the ClickUp notification (step 8), then stop.

## 0. Config

Read `~/.claude/content-config.json`. On the first interactive run, ask for whatever is missing, one question at a time, and save it:

```json
{
  "content_folder": "/Users/<name>/Library/CloudStorage/GoogleDrive-<email>/My Drive/La Luna Content",
  "language": "Deutsch",
  "posts_per_day": 7,
  "sales_calls": "Meet Recordings",
  "whatsapp_skip": ["Mama", "Family group"],
  "photo_folder": "/Users/<name>/Library/CloudStorage/GoogleDrive-<email>/My Drive/La Luna Content/Fotos",
  "brand": {"background": "#F4E9E1", "text": "#3B2A2F", "accent": "#B5838D", "handle": "@lalunafertility"},
  "clickup_list": "Content"
}
```

- `sales_calls`: the Google Drive folder where Google Meet saves call transcripts. Read it through the Google Drive connector. If the connector isn't available, read the same folder on disk under Google Drive for Desktop, where `.txt` and `.docx` files are readable but Google Docs (`.gdoc`) are not.
- `whatsapp_skip`: chats never used as material, such as family and friends.
- `photo_folder` is optional: photos of the owner and the practice that cards can use.
- `brand`: colours as hex values and the Instagram handle. Look at their Instagram or website for the colours, then confirm them.
- `clickup_list`: the ClickUp list that gets the "carousels ready" task. Leave it empty to skip ClickUp.

Then read `<content_folder>/brand-voice.md` in full. If it's missing, run the `brand-voice` skill first. On a scheduled run, treat it as a blocker.

## 1. Gather what's new

`<content_folder>/used.json` records the last run and what has been used: `{"last_run": "<ISO time>", "ideas": [...], "calls": [...], "whatsapp": [...]}`. Gather only material newer than `last_run` (the last 3 days on a first run):

1. **Spoken ideas:** new bullets in `<content_folder>/Ideas.md`. These come first: the owner chose them.
2. **Sales calls:** new transcripts in the `sales_calls` folder. Pull out the client's questions, fears, objections and exact phrases, and what the owner answered.
3. **WhatsApp:** `list_chats`, then `read_chat` on each chat active since `last_run` that isn't in `whatsapp_skip`. Pull out the same: questions, pain points, phrases, and voice notes in which the owner explains something well.

**Privacy, always:** clients and prospects are never named, quoted in a way that identifies them, or described with details someone could recognise. A post turns "a client asked X" into the question itself. Health details stay general.

## 2. Pick the posts

Choose `posts_per_day` posts (5 to 10), each built on **one** idea: one question, one mistake, one myth, one number, one story. A list of loosely related tips is not a post.

Rank by how many people the idea helps and how strongly it hits: a question asked by several prospects beats one asked once, and a spoken idea beats both. If there's too little new material, fall back on the stories and opinions in `brand-voice.md` and say so in the day's README. Never pad with generic advice.

## 3. Write each carousel

Write in `language`, in the voice of `brand-voice.md`, and keep to every rule in its sections 9 and 10.

- **6 to 10 slides.** Instagram re-shows a skipped carousel starting at slide 2, and reach to new people comes mainly from sends, so:
  - **Slide 1, the cover:** a headline a stranger understands with no context and wants to swipe for, ideally with a number or a direct question. Add a small `kicker` line above it saying who it's for ("Kinderwunsch seit über einem Jahr?"). No "Tipps zum Thema X" covers.
  - **Slide 2, a second cover:** hooks on its own, usually why this matters or the most surprising line.
  - **Middle slides:** each one sentence or short paragraph that moves the story on and leads to the next slide. Under 30 words a slide.
  - **Second-to-last slide:** the takeaway in 3 short numbered lines, something worth saving, ending with a send prompt aimed at a person ("Schick das einer Freundin, die gerade mittendrin steckt").
  - **Last slide:** the one action from `brand-voice.md` (book a call, send a DM with a keyword, follow).
- **No emoji on slides**, because the card font can't draw them. Emoji can go in the caption, as `brand-voice.md` allows.
- **Caption:** the first line restates the cover in plain words with the topic's search words in it, then 3 to 6 short paragraphs or a short list that add to the slides rather than repeat them, then the call to action. No hashtags.
- **Photos:** if `photo_folder` holds a photo that fits a slide, especially one of the owner for the cover or the last slide, set it as that slide's `photo`. Look at the photos before choosing. Otherwise use the brand background.

## 4. Critique, at most two rounds

Hand the whole batch to a fresh subagent with no other context: `brand-voice.md`, every post's slide text and caption, and these questions:

1. Would a stranger scrolling past stop for this cover? Rate each cover 1 to 10 and rewrite any under 7.
2. Does every sentence sound like the reference lines in `brand-voice.md`? Quote the ones that don't.
3. Is anything invented, exaggerated, medically promised or identifying a client?
4. Any dashes, semicolons, contrast pairs, teaser hooks, moral closers or banned words?

Apply the fixes and run it once more if the first round changed a lot.

## 5. Render

For each post, write `slides.json` into its folder in the shape documented at the top of `render_cards.py` (next to this file), using the `brand` from the config, then run:

```bash
uv run "<this skill's folder>/render_cards.py" "<post folder>"
```

Look at `cards/strip.jpg`. If a slide's text is too long or a pill covers a face, shorten the text or change the photo and render again.

## 6. Save

```
<content_folder>/Carousels/<YYYY-MM-DD>/
  README.md                  the day at a glance: each post's cover line, its source, and anything to check
  01-<short-slug>/
    cards/slide-01.png ...   the slides, ready to upload in order
    cards/strip.jpg          all slides in a row, for a quick look
    caption.md               the caption, ready to paste
    brief.md                 the idea, where it came from (no names), and the critique's notes
    slides.json
```

Then update `used.json` with this run's time and the ideas, calls and chats used.

## 7. Done

Say in two or three lines how many carousels were made, where they are, and anything that needs a human eye (for example a fact to confirm).

## 8. ClickUp notification

If `clickup_list` is set and ClickUp tools are available (the ClickUp connector), create one task in that list: "<n> Karussells bereit: <date>". Its description lists each post's cover line and the path to the day's folder. If ClickUp isn't connected, skip this and mention it in step 7.

## Running it every morning

Scheduling lives in the app, not in this skill. In T3 Code, ask: "Schedule /content:daily-carousels every day at 6:00 in this project." The Mac has to be on, awake and logged in at that time, with T3 Code open: in System Settings > Battery, set the Mac not to sleep while on power, and leave it plugged in overnight.
