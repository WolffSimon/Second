#!/usr/bin/env bash
# Run one cold review round with Claude Code, headless, in an empty temporary folder.
#
# Usage: bash scripts/review_round.sh JD.txt CV.txt STYLE_GUIDE.md ["description of the reader"] > report.md
#
# The three files are copied into a fresh folder and Claude Code runs there in "dontAsk" mode:
# reads inside that folder are allowed, anything that would need approval is refused, so the
# reviewer cannot open your archive. If ANTHROPIC_API_KEY is set, --bare is added, which also
# skips your CLAUDE.md, skills, hooks and plugins. Without it, ~/.claude/CLAUDE.md will load.
set -euo pipefail
# Treat "&" in replacements literally (bash 5.2 and later would otherwise expand it).
shopt -u patsub_replacement 2>/dev/null || true

if [ $# -lt 3 ]; then
  echo "usage: bash $0 JD.txt CV.txt STYLE_GUIDE.md [\"description of the reader\"]" >&2
  exit 2
fi
command -v claude >/dev/null || { echo "Claude Code CLI not found on PATH" >&2; exit 2; }

here="$(cd "$(dirname "$0")/.." && pwd)"
brief="$here/skills/cold-review-loop/references/reviewer_brief.md"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

cp "$1" "$work/job_description.txt"
cp "$2" "$work/cv.txt"
cp "$3" "$work/style_guide.md"
reader="${4:-}"

# The brief is everything after the first line consisting of three dashes.
prompt="$(awk 'found { print } /^---$/ { found = 1 }' "$brief")"
prompt="${prompt//\{JD_PATH\}/job_description.txt}"
prompt="${prompt//\{CV_PATH\}/cv.txt}"
prompt="${prompt//\{STYLE_PATH\}/style_guide.md}"
if [ -n "$reader" ]; then
  prompt="${prompt//\{READER\}/$reader}"
else
  prompt="${prompt// \[\{READER\}\]/}"
fi

flags=(-p "$prompt" --permission-mode dontAsk --output-format text)
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  flags=(--bare "${flags[@]}")
else
  echo "note: ANTHROPIC_API_KEY is not set, so the review runs without --bare and ~/.claude/CLAUDE.md will load" >&2
fi

cd "$work"
claude "${flags[@]}" < /dev/null
