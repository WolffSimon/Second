# Changelog

## 2.0, October 2026

- **The cold review loop.** Every finished document now goes to a fresh reviewer that sees only the job description, the CV as text and the style guide. Findings are triaged (accept, reject with a reason, ask the person), fixes are checked against the inventory, and rounds repeat with a new reviewer until a round finds nothing of high or medium severity that the builder can fix, or three have run. New: `WORKFLOW.md`, `skills/cold-review-loop`, `.claude/agents/cold-reviewer.md`, `scripts/review_round.sh`, `scripts/export_cv_text.py`.
- **Parallel builds** for a wave of postings, with one writer to the inventory.
- **Prose law** brought up to date: role entries in prose, Stack lines on technical seats, a warning against fixing one style fault with another device, letters in ordinary business English, workshop words kept out of documents, the normative test, and plainer names for most rules.
- **CV build** rewritten around the protocol order, with cold review as its last step and keyword blocks only where a machine reads first.
- **Master prompt** split into the method, which stays fixed, and your own standing orders, which are examples to keep or replace.
- **Archive templates** for the style guide, inventory, cast list and project context. The style guide template holds writing rules only, so it is safe to show a reviewer.
- **Scripts:** `add_education_tools.py` now reads a JSON file and is idempotent; `check_document.py` flags sentences without a finite verb and treats repeated numbers as advisory; `build_dist.sh` rebuilds the skill zips.
- **Setup notes** updated for uploading skills to Claude.ai and installing skills and subagents in Claude Code.
- Every example in the skills and templates is a placeholder.

## 1.0, September 2026

First release: eight skills, a master prompt, a runbook and Word-document scripts.
