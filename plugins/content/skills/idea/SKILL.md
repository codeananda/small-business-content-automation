---
name: idea
description: Save a content idea for later. Use when someone says "/idea ...", "I have an idea for a post", "Idee für einen Post", or dictates a thought they want turned into content. Appends it to Ideas.md in the content folder so the daily carousel run picks it up.
---

# Save an idea

1. Find the content folder: read `~/.claude/content-config.json` and use its `content_folder`. If the file doesn't exist, ask once where the content folder should be (suggest `My Drive/La Luna Content` inside Google Drive), create the folder and write `{"content_folder": "<absolute path>"}` to the config file. `/daily-carousels` fills in the rest of the config on its first run.
2. Append the idea to `<content_folder>/Ideas.md` as one bullet: `- YYYY-MM-DD: <the idea>`. Create the file with the heading `# Ideas` if it's missing.
3. Keep their words. Fix obvious dictation errors only, keep the language they spoke in, and don't polish it into a post. If they rambled, keep the whole thought: the details are what make a good post later.
4. If they asked for research ("look into this", "recherchier das"), do a short web search and add two or three facts with their sources as indented sub-bullets under the idea.
5. Reply in one line: the idea is saved and will be in tomorrow's carousels.
