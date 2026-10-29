# Shareable skills

Claude Code plugins from Adam Murphy, packaged so they install on anyone's Mac without Homebrew. They work in T3 Code, in Claude Code Desktop and in the terminal.

## Set up a Mac

Open Terminal, paste this line and press Enter:

```bash
curl -fsSL https://raw.githubusercontent.com/codeananda/shareable-skills/main/setup.sh | bash
```

It installs Claude Code, uv and the plugins, adds a starter list of permissions so Claude asks "allow?" less often, and opens the pages for the steps a script can't do for you. It never asks for your password and is safe to run again.

What you do by hand afterwards:

1. Install T3 Code from [t3.codes/download](https://t3.codes/download) and log in to Claude.
2. In T3 Code, under Settings > Providers > Claude, type `--chrome` in Launch arguments.
3. Install WhatsApp from the App Store and link it to your phone.
4. In System Settings > Privacy & Security > Full Disk Access, add T3 Code and switch it on, then quit and reopen T3 Code.

## Plugins

| Plugin | What it does | Needs |
|---|---|---|
| `whatsapp-reader` | Reads your WhatsApp chats on this Mac and transcribes voice notes in German and English on the Mac's GPU. Read-only; nothing leaves the Mac except what Claude is shown. | Apple Silicon (M1 or newer), macOS 14 or later, about 5 GB free disk. The 1.6 GB speech model downloads the first time it transcribes. |

To update to the latest versions: `claude plugin marketplace update shareable-skills`.

## For Adam: adding a plugin

1. Make `plugins/<name>/` with a `.claude-plugin/plugin.json` and its skills or servers.
2. List it in `.claude-plugin/marketplace.json`.
3. Run `claude plugin validate .` and test with `claude -p "..." --plugin-dir plugins/<name>`.
4. If it should install for everyone, add a `claude plugin install <name>@shareable-skills` line to `setup.sh`.

`plugins/whatsapp-reader/manifest.json` also lets the same folder build the Claude Desktop extension: `npx @anthropic-ai/mcpb pack plugins/whatsapp-reader`.
