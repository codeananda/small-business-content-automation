---
name: brand-voice
description: Build or update brand-voice.md, the file that makes every post sound like the person behind the business and not like AI. Use when someone says "/brand-voice", "set up my brand voice", "analyse how I speak", "Markenstimme", or hands over transcripts of their videos, podcasts or calls. Also use when /daily-carousels finds no brand-voice.md.
---

# Brand voice

The goal is a file that captures how this person actually talks, from their own words, so that a sentence written for them reads as if they said it. Every content skill reads `brand-voice.md` before it writes anything.

## 1. Find the content folder

Read `~/.claude/content-config.json` and use its `content_folder`. If it's missing, ask where the content folder should be (suggest `My Drive/La Luna Content` inside Google Drive), create it and write `{"content_folder": "<absolute path>"}` to the config. If `brand-voice.md` already exists there, read it and ask whether to add to it or start fresh.

## 2. Gather their real words

Ask for sources and take whatever they give. More is better, and 20 minutes or more of speech is enough for a good file:

- **Transcripts of videos, reels, podcasts or lives** where they talk to camera. These are the best source. Pasted text, files in a folder, or Google Docs via the Google Drive connector all work. YouTube shows a transcript under a video's description (`...more` > Show transcript), and Instagram reels can be transcribed by downloading the video and asking Claude to transcribe it.
- **Sales call transcripts** from the Google Meet folder in Drive. Use only the lines the owner says, never the client's.
- **WhatsApp messages they sent**, through the WhatsApp tools (`read_chat`). These show how they write as opposed to how they speak.
- **Captions they already like** from their own Instagram.

Don't use AI-written posts or anything a copywriter wrote as a source: they teach the file the wrong voice.

Also ask these four questions, one at a time, if the sources don't answer them:
1. What do you sell, in plain words, and who is the one kind of person who buys it?
2. What's the one thing you want someone to do after reading a post (book a call, send a DM, follow)?
3. What's an opinion you hold about your field that most people in it would push back on?
4. Are there words, claims or topics that must never appear in your posts?

## 3. Analyse

Read everything. Note what they really do, with examples quoted word for word:

- **Rhythm:** sentence length, how they join thoughts ("und", "also", "weil", "and", "so"), how they start and end a point.
- **Address:** du or Sie, first names, how they greet and sign off.
- **Words and phrases they use often**, and their pet expressions.
- **Words they never use**, and anything that would sound wrong from them (often brand speak).
- **Humour, warmth and excitement:** how each shows up, and how much.
- **How they deliver hard truths or bad news.**
- **Punctuation and emoji** in what they write: which emoji, how many, exclamation marks.
- **Stories and examples they keep returning to.** These become post material.

## 4. Write brand-voice.md

Write it in the language they create content in (German for La Luna). Use this shape:

```markdown
# Brand voice: <business>

Built on <date> from <list of sources>. The target in one line: <who is talking to whom, e.g. "Sina talking to a friend who has been trying for a baby for a year">.

## Business
What they sell, who buys, the one action a post asks for, the opinion that sets them apart.

## 1. Rhythm
## 2. How they address the reader
## 3. Words they use
## 4. Never say
## 5. Warmth, humour and hard truths
## 6. Punctuation and emoji
## 7. Verbatim reference lines
10 to 15 lines quoted exactly from the sources. A new sentence that would look odd next to these gets rewritten.
## 8. Stories and examples they return to
## 9. Rules for every post
## 10. Check before publishing
A short checklist drawn from sections 1 to 9.
```

Section 9 always carries these rules, because they are what make text read as AI-written. Add the person's own on top:

- Read every sentence aloud in their voice. If they wouldn't say it like that to a friend, rewrite it.
- Vary sentence length. Join related short sentences with a linking word. Never three or more short sentences of similar length in a row.
- No contrast pairs ("Not X. Y.", "X is one thing. Y is another."), no teaser hooks that promise a payoff ("here's what happened", "du wirst nicht glauben"), no tidy one-line moral at the end, no staccato runs.
- No dashes of any kind (— or –) and no semicolons. Use a comma or a linking word.
- No clichés, metaphors or generalisations. Use real numbers and real examples from the sources.
- No hashtags or markdown in the post body.
- Every fact and number exactly as sourced. Never invent a client story, a statistic or a result.
- At most one exclamation mark per post. Excitement goes into the words.
- Keep these words out, and their German equivalents: game-changer, unlock, journey, delve, empower, transformative, embark, elevate, crafted, seamless, revolutionise, "in today's world", "Reise", "Gamechanger", "transformieren", "auf das nächste Level".

For a health or fertility business, also add: no promise of a pregnancy or a medical outcome, no diagnosis, and no claim that isn't backed by a source.

## 5. Confirm

Show them the reference lines and the one-line target, and ask whether that sounds like them. Fix what they say is off. Tell them to run `/brand-voice` again whenever they have new transcripts, since the file gets better with more of their words.
