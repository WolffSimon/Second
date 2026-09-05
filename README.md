# Second

A human-first, AI-augmented job search. By Matthew Wolff Simon. A work coach built with Claude: the second in your corner, not the fighter in the ring. This project is independent and is not affiliated with, endorsed by or sponsored by Anthropic; "Claude" is used only to name the assistant it is designed to work with.

A method for running a senior job search with an AI assistant as staff, not as oracle. The human decides; the assistant writes, checks, records and asks. Everything here was built in a live search and refined against real rejections.

## Preface

In running a job search and application process for several months, with Claude as staff, I came to some realisations. If you ask Claude to help you apply for a job, it will select the right qualifications for the application and write you a good CV. That is the easy part, and it is also the dangerous part. Mass applying at the fastest possible speed is bad for everyone. It overcrowds recruiters and it gives them low-quality CVs, and a low-quality CV with your name on it is worse than none.

Claude is an excellent tool with syndromes that work against showing what you have done. It reassures. It advises you to rest, to eat and to sleep, and it puts you to bed with some regularity. It sometimes balks at a job because it judges the seat beneath you, or the salary out of line with objectives you never stated. It writes in noun phrases of the Robert Ludlum kind, so that a review becomes the Benares Review Exercise. It reaches for cliché and metaphor. It conflates different skills and achievements into composites that misrepresent you. It favours narrative over clarity and introduces you through your first job, your humble start and your origin story. Once it has coined a phrase for one application it reuses it in the next, so a helpful note that a rural office is fifteen minutes from your house appears in every application thereafter, relevant or not. And in an industry with jargon, it keeps the jargon.

So I built this. A master prompt, which you ask it to consult every time the context is compacted, indexes everything else and carries the standing orders. A style guide improves the writing of CVs, notes and letters considerably. An inventory of accomplishments is the place you bank what you excavate from a long career. A dramatis personae keeps the people straight. An excavation skill exists because a model assumes that what it knows about you is everything about you, and will assume you lack experience you have. The second pass skill is the most valuable thing here: it reviews what has been written against the style guide and the job description, looks in your inventory for what is missing, and asks you for the rest.

The aim is to give you the best presentation you can make, to give recruiters the best information about you, and to make an AI a work coach and not a mass supplier of applications without context.

## Deploying into Claude

**In Claude.ai (web and desktop; a paid plan is required for custom skills).** Zip each skill folder on its own, so that the zip contains the folder with `SKILL.md` inside it, then go to Settings, Capabilities, Skills, and upload each zip. The uploader takes one skill per zip. The `name` in each `SKILL.md` is lowercase with hyphens and matches its folder name, and each description is under 200 characters, which Claude.ai requires. Ready-made zips for each skill are in `dist/`.

**The master prompt and the archive.** Create a Project. Paste `MASTER_PROMPT.md`, with your details filled in, into the Project's instructions. Add your private archive files to the Project's knowledge: your style guide, your accomplishments inventory, your dramatis personae and your project context. Whenever a long conversation is compacted, tell Claude to run the master prompt again; the skills persist, but the scene does not.

**In Claude Code.** Copy the `skills/` folders into `.claude/skills/` in your working directory or `~/.claude/skills/` for all projects, or use `npx skills add <your-github-user>/<this-repo>` once you have published it.

**Scripts.** `scripts/check_document.py` needs `python-docx`, and LibreOffice on the path for the page count. `scripts/docx_helpers.py` assumes a table-based CV template with bullet paragraphs styled "List Paragraph"; adjust the style name if yours differs.

## What this is

Second is eight skills, a master prompt and an order of operations. The name is the boxer's second, the coach in the corner who watches, advises and hands you the towel; it is also the second pass, the skill that matters most. Each skill is a `SKILL.md` in the format used by Claude Skills: a name, a description that says when it applies, and a body that says how. Some carry `references/` and `scripts/`.

- `MASTER_PROMPT.md` — run at the start of every session and after every context compaction. It sets the roles, the archive, the laws and the standing orders.
- `RUNBOOK.md` — the order of operations for a new job description, a voice note, an application form, a recruiter note and a journal update.
- `skills/prose-law` — the writing law. The other skills obey it. This is the important one.
- `skills/cv-build-from-jd` — from a job description to a finished CV.
- `skills/excavation-interview` — questions that surface experience the file does not hold.
- `skills/receipts-inventory` — how to keep the accomplishments inventory the build depends on.
- `skills/second-pass-rubric` — the check that turns a draft into a document.
- `skills/voice-note-to-document` — dictate on a walk, return to a document.
- `skills/recruiter-notes` — direct messages and emails to recruiters and hiring managers.
- `skills/compliance-journal` — the dated activity record a benefits or work-coach journal needs.
- `scripts/` — Word document helpers and a checker for banned phrases, repeated numbers and page count.

## The two layers

The method is public. The archive it runs on is private and never published: the inventory of a real person's receipts, the cast of recruiters and colleagues, the correspondence. Every example in these skills is a placeholder. If you adopt the method, your archive stays yours.

## Principles, in one paragraph

Open on the receipt. Say what you did, with a subject and a verb. State each number once. Never invent, and never let true facts compose into a claim you did not make. Read the prose law before every build; it does not survive being summarised. Ask questions before assuming a gap, because absence from the file is not absence from the career. Give a number with its reasoning and stop. Odds move on events, not on the calendar. Record new facts the day they are disclosed. When wrong, say what was wrong, fix it and record it.

## Licence

Prose and skills: CC BY 4.0. Scripts: MIT. See `LICENSE`.
