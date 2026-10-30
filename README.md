# Small business content automation

Claude Code plugins that write a small business's Instagram carousels every morning, in the owner's own voice, from the raw material they already have: WhatsApp chats with prospects, sales call transcripts and ideas spoken on the fly. Built for La Luna Fertility. It runs in T3 Code, in Claude Code Desktop and in the terminal, and it never posts anything by itself.

## Set up a Mac

Open Terminal, paste this line and press Enter:

```bash
curl -fsSL https://raw.githubusercontent.com/codeananda/small-business-content-automation/main/setup.sh | bash
```

It installs Claude Code, uv and the plugins, adds a starter list of permissions so Claude asks "allow?" less often, and opens the pages for the steps a script can't do for you. It never asks for your password and is safe to run again.

What you do by hand afterwards:

1. Install T3 Code from [t3.codes/download](https://t3.codes/download) and log in to Claude.
2. In T3 Code, under Settings > Providers > Claude, type `--chrome` in Launch arguments.
3. Install WhatsApp from the App Store and link it to your phone.
4. In System Settings > Privacy & Security > Full Disk Access, add T3 Code and switch it on, then quit and reopen T3 Code.
5. Install [Google Drive for Desktop](https://www.google.com/drive/download/) so the carousels land in your Drive.

## First steps in T3 Code

1. **Make your brand voice file.** Type `/content:brand-voice`. Have transcripts ready of you talking: reels, videos, podcast episodes, lives or sales calls. The more of your own words it reads, the more the posts sound like you. Run it again whenever you have new transcripts.
2. **Make today's carousels.** Type `/content:daily-carousels`. The first run asks where things live (content folder, sales call folder, brand colours, ClickUp list) and remembers the answers.
3. **Run it every morning.** Ask Claude: "Schedule /content:daily-carousels every day at 6:00 in this project." Leave the Mac plugged in and awake overnight with T3 Code open.
4. **Save ideas as they come.** Type `/content:idea` followed by the idea, or dictate it. Tomorrow's run picks it up first.

## Plugins

| Plugin | What it does | Needs |
|---|---|---|
| `content` | `/content:brand-voice` builds `brand-voice.md` from your transcripts. `/content:idea` saves an idea. `/content:daily-carousels` turns new ideas, sales calls and WhatsApp chats into 5 to 10 carousels (cards, caption, brief) in a dated Google Drive folder and adds a "ready" task in ClickUp. | Google Drive for Desktop. The Google Drive and ClickUp connectors in Claude for the sales calls and the notification. |
| `whatsapp-reader` | Reads your WhatsApp chats on this Mac and transcribes voice notes in German and English on the Mac's GPU. Read-only; nothing leaves the Mac except what Claude is shown. | Apple Silicon (M1 or newer), macOS 14 or later, about 5 GB free disk. The 1.6 GB speech model downloads the first time it transcribes. |

To update to the latest versions: `claude plugin marketplace update small-business-content-automation`.

## For Adam: adding a plugin

1. Make `plugins/<name>/` with a `.claude-plugin/plugin.json` and its skills or servers.
2. List it in `.claude-plugin/marketplace.json`.
3. Run `claude plugin validate .` and test with `claude -p "..." --plugin-dir plugins/<name>`.
4. If it should install for everyone, add a `claude plugin install <name>@small-business-content-automation` line to `setup.sh`.

`plugins/whatsapp-reader/manifest.json` also lets the same folder build the Claude Desktop extension: `npx @anthropic-ai/mcpb pack plugins/whatsapp-reader`.

The card font is Montserrat, under the SIL Open Font License (`plugins/content/skills/daily-carousels/fonts/OFL.txt`).
