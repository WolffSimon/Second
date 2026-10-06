# Second

A human-first, AI-assisted job search. Second is a method and a toolset for running a senior job search with Claude as staff. The person decides. The assistant writes, checks, records and asks. A second assistant, which has seen none of the work, reviews every document cold before it goes out.

The name is the boxer's second: the coach in the corner who watches, advises and hands over the towel, but never throws a punch. It is also the second pass, the check that turns a first draft into a document.

This project is independent. It is not affiliated with, endorsed by or sponsored by Anthropic. "Claude" is used only to name the assistant it was built to work with.

## Why it exists

Ask an AI assistant to help with a job application and it will write a plausible CV in seconds. That is the easy part, and it is also the dangerous part. Mass applications at speed are bad for everyone: they crowd recruiters' inboxes, and a weak CV with your name on it does more harm than no CV at all.

Second was built over several months of a live senior search and refined against real rejections. Along the way the assistant showed habits that work against showing what a person has done:

- It reassures, and suggests a rest, when you asked for a document.
- It judges a role beneath you, or a salary out of line, against objectives you never stated.
- It writes in strings of nouns, so a review becomes "the operational resilience review exercise".
- It reaches for metaphor and cliché.
- It assembles true facts into composite claims you never made.
- It introduces you through your first job and your origin story.
- It reuses a phrase coined for one application in every application after it.
- It keeps the jargon of the last industry it read about.
- It assumes that what it knows about you is everything you have done.
- It marks its own work, and passes it.

Each part of Second answers one of these.

## Getting started

Read in this order: this README, `MASTER_PROMPT.md`, `RUNBOOK.md`, `skills/prose-law/SKILL.md`, then `WORKFLOW.md`. The other skills are read when a step calls for them.

Then, for a first session:

1. Copy the four files in `archive-templates/` into a private folder (call it `archive/`; it is excluded from git here). Fill in the project context and the cast list. Paste the prose law into the style guide where the template says.
2. Start the inventory. The fastest way is to give Claude your current CV and ask it to run `excavation-interview` against it, era by era. Bank every answer in your own words.
3. Fill in `MASTER_PROMPT.md` and set it up as described below.
4. Give Claude a job description and ask for an assessment. If you want the role, ask for a build. The build runs the protocol and the second pass. In Claude Code the builder then runs the cold review rounds itself; in Claude.ai you carry each round to a new chat and bring the report back. Either way you end with a document and a short list of questions.
5. Answer the questions. Claude banks the answers, applies them and runs one final review.

## What is in the box

| Path | What it is |
|---|---|
| `MASTER_PROMPT.md` | The standing instructions: the roles, the archive, the method and your own standing orders. |
| `RUNBOOK.md` | The order of operations: a new job description, a wave of postings, a voice note, a rejection. |
| `WORKFLOW.md` | The agentic loop: a build, a cold review and a triage, in rounds, until the document is clean; and how to run several builds in parallel. |
| `skills/prose-law` | The writing law. Every other skill obeys it. This is the important one. |
| `skills/cv-build-from-jd` | From a job description to a finished CV, in protocol order. |
| `skills/cold-review-loop` | The review rounds: the reviewer brief, triage rules, stop rules and a triage log. |
| `skills/second-pass-rubric` | The builder's own check: unanswered requirements, the inventory searched, questions asked. |
| `skills/excavation-interview` | Questions that surface experience the archive does not yet hold. |
| `skills/receipts-inventory` | How to keep the accomplishments inventory that every build depends on. |
| `skills/recruiter-notes` | Notes and messages to recruiters, hiring managers and referrers. |
| `skills/compliance-journal` | A dated work-search record, for a benefits system, an outplacement coach or your own discipline. |
| `skills/voice-note-to-document` | Dictate on a walk; come back to a document. |
| `.claude/agents/cold-reviewer.md` | The reviewer as a Claude Code subagent, with read-only tools and without your `CLAUDE.md`. |
| `archive-templates/` | Empty starting files for your private archive. |
| `scripts/` | Word-document helpers, a prose checker, a CV-to-text exporter, a headless review script and a script to rebuild `dist/`. |
| `dist/` | One zip per skill, ready to upload to Claude.ai. |

## The two layers

The method is public. The archive it runs on is private and is never published.

Your archive holds four files: a style guide (the prose law plus your own writing rulings), an accomplishments inventory, a cast list of the people in your search, and a project context with the live board and any facts about you that documents must state in one way only. Keep writing rules and personal facts apart: the cold reviewer reads your style guide, and must never read anything personal. Every example in the skills is a placeholder.

## The loop, in one paragraph

The builder reads the job description, reads the whole inventory, builds the CV from scratch, runs the prose law and its own second pass, and checks the result. Then a fresh reviewer receives three files and nothing else: the job description, the CV as plain text and the style guide. It reports a verdict, numbered findings and the three things nobody should cut. The builder triages every finding: accept, reject with a reason, or turn it into a question for you. It checks every accepted change against the inventory and never adds a fact on a reviewer's say-so. A new reviewer runs the next round. The builder stops when a round returns no high or medium finding that it can fix from the archive, or after three rounds, and brings you the remaining questions. After you answer, one final round runs. `WORKFLOW.md` has the detail.

## Setting up

### Claude.ai (web and desktop)

1. Upload the skills. Go to Customize, then Skills, choose Add, and upload each zip from `dist/`. Each zip holds one skill folder with its `SKILL.md` at the root. Code execution must be enabled for skills to work. Skill names are lowercase with hyphens and under 64 characters, and each description is under 200 characters, as Claude.ai requires.
2. Create a Project for the search. Paste `MASTER_PROMPT.md`, with your details filled in, into the Project's instructions. Add `RUNBOOK.md`, `WORKFLOW.md` and your four archive files to the Project's knowledge.
3. For cold reviews, open a new chat outside the Project, so the reviewer cannot see your archive. If your account has memory turned on, use an incognito chat, so the reviewer cannot draw on it either. Paste the brief from `skills/cold-review-loop/references/reviewer_brief.md`, attach the three files it names, and replace the three paths in the brief with the names of the attachments.

The Python scripts are not part of the skill zips. In Claude.ai, the skills tell Claude to make the same checks by reading.

Whenever a long conversation is compacted, ask Claude to re-read the master prompt. The skills persist; the working context does not.

### Claude Code

1. Copy each folder in `skills/` into `.claude/skills/` in your working directory, or into `~/.claude/skills/` for every project.
2. Copy `.claude/agents/cold-reviewer.md` into `.claude/agents/` (or `~/.claude/agents/`). A subagent starts with a fresh context, so the builder can hand each review to it. This one has read-only tools and is set not to load `CLAUDE.md`.
3. Keep your archive in a folder such as `archive/`, and paste the filled-in master prompt into the project's `CLAUDE.md` or into your first message.
4. For a review from the command line, run `bash scripts/review_round.sh` (see `WORKFLOW.md`).

### Scripts

```
pip install python-docx
```

The page count in `check_document.py` also needs LibreOffice (`soffice`) and `pdfinfo` on the path. `docx_helpers.py` assumes a CV built on tables, with the role entries as paragraphs styled "List Paragraph"; change the style name if yours differs. `check_document.py` works on any `.docx`. `export_cv_text.py` is built for the same table template but also exports plain paragraphs. `review_round.sh` needs the Claude Code CLI. `build_dist.sh` rebuilds the zips in `dist/` after you edit a skill.

## Terms used

- **Receipt.** A specific thing you did, with a number or a name attached, which a reader could check.
- **Inventory.** Your private file of receipts, dated and in your own words. It is canon: documents are built from it, and a fact that is not in it does not go on a page.
- **Cast list.** Your private file of the people in your search: recruiters, hiring managers, referrers, with notes on how to handle each.
- **Builder.** The main Claude session, which has your archive and writes the documents.
- **Reviewer.** A fresh Claude session or subagent that sees only the job description, the CV and the style guide.
- **Triage.** Deciding, for each reviewer finding, whether to accept it, reject it with a reason, or ask you.
- **Bank.** To record a new fact in the inventory, dated and in your own words, on the day you disclose it.
- **Rated base document.** A CV for one family of roles that has been reviewed and that you are content with. New builds copy its layout, never its wording.
- **Knife pass.** A cutting pass over a draft: anything irrelevant, decorative, borrowed or repeated comes out.
- **Seat.** The role being applied for.
- **Live board.** The list of open processes, their stage and the next step for each.

## Principles, in one paragraph

Open on the receipt: say what you did, with a subject and a verb. State each number once unless the sentence needs it twice. Never invent, and never let true facts compose into a claim you did not make. Read the prose law before every build, because it does not survive being summarised. Ask before assuming a gap, because absence from the file is not absence from the career. Let someone who has not seen the work read it before a recruiter does. Give a number with its reasoning and stop. Record new facts the day they are disclosed. When wrong, say what was wrong, fix it and record it.

## Licence

Prose and skills: CC BY 4.0. Scripts: MIT. See `LICENSE`.
