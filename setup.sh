#!/bin/bash
# Sets up Claude Code on a Mac with the content and WhatsApp plugins. No Homebrew, no password. Safe to run again.
#   curl -fsSL https://raw.githubusercontent.com/codeananda/small-business-content-automation/main/setup.sh | bash
# Pass a local checkout to install from it instead of GitHub: bash setup.sh /path/to/small-business-content-automation
set -euo pipefail

MARKETPLACE="${1:-codeananda/small-business-content-automation}"
SETTINGS="$HOME/.claude/settings.json"
# Every place an existing Claude Code or uv may live, so nothing already installed gets installed again.
export PATH="$HOME/.local/bin:$HOME/.claude/local:/opt/homebrew/bin:/usr/local/bin:$PATH"

echo "== 1/6 Checking this Mac"
macos_major=$(sw_vers -productVersion | cut -d. -f1)
if [ "$(uname -m)" = arm64 ] && [ "$macos_major" -ge 14 ]; then
  whatsapp_ok=1
else
  whatsapp_ok=0
  echo "!! The WhatsApp reader needs an Apple Silicon Mac (M1 or newer) on macOS 14 or later. Skipping it."
fi

echo "== 2/6 Apple's command line tools (for downloading plugins)"
if ! xcode-select -p >/dev/null 2>&1; then
  xcode-select --install || true
  echo "   A window has opened. Click Install and wait for it to finish; this script carries on by itself."
  until xcode-select -p >/dev/null 2>&1; do sleep 10; done
fi

echo "== 3/6 Claude Code and uv"
if command -v claude >/dev/null; then echo "   Claude Code already installed, skipping."; else curl -fsSL https://claude.ai/install.sh | bash; fi
if command -v uv >/dev/null; then echo "   uv already installed, skipping."; else curl -fsSL https://astral.sh/uv/install.sh | sh; fi

echo "== 4/6 Plugins"
claude plugin marketplace add "$MARKETPLACE" >/dev/null 2>&1 || claude plugin marketplace update small-business-content-automation
claude plugin install content@small-business-content-automation
if [ "$whatsapp_ok" = 1 ]; then
  claude plugin install whatsapp-reader@small-business-content-automation
fi

echo "== 5/6 Fewer \"allow?\" questions"
# Adds to the allow list and keeps everything already in the settings file.
uv run --quiet --no-project python - "$SETTINGS" <<'EOF'
import json, sys
from pathlib import Path

path = Path(sys.argv[1])
settings = json.loads(path.read_text()) if path.exists() else {}
allow = settings.setdefault("permissions", {}).setdefault("allow", [])
# Write, Edit and the uv/mkdir commands let the scheduled carousel run finish without anyone clicking "allow".
for rule in ["Read", "Glob", "Grep", "Write", "Edit", "WebSearch", "WebFetch", "Skill",
             "Bash(uv run:*)", "Bash(mkdir:*)", "Bash(ls:*)",
             "mcp__plugin_whatsapp-reader_whatsapp", "mcp__claude_ai_Google_Drive", "mcp__claude_ai_ClickUp"]:
    if rule not in allow:
        allow.append(rule)
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(settings, indent=2) + "\n")
EOF

echo "== 6/6 Opening the pages for the last steps"
open "https://t3.codes/download"
open "https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn"
[ "$whatsapp_ok" = 1 ] && open "macappstore://apps.apple.com/app/whatsapp-messenger/id310633997"
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"

cat <<'EOF'

Done. The last steps, by hand:
  1. Install T3 Code from the page that opened, then open it and log in to Claude when it asks.
  2. In T3 Code, go to Settings > Providers > Claude and type --chrome under Launch arguments.
  3. Add the Claude extension to Chrome from the page that opened, and sign in with the same Claude account.
  4. Install WhatsApp from the App Store and link it to your phone.
  5. In the Full Disk Access window, click +, choose T3 Code from Applications and switch it on.
     Then quit T3 Code and open it again.
  6. Install Google Drive for Desktop: https://www.google.com/drive/download/
  7. In T3 Code, type /content:brand-voice to build your brand voice file, then /content:daily-carousels.
EOF
