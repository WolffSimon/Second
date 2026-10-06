---
name: cold-review-loop
description: Run rounds of cold review on a finished CV: a fresh reviewer with three files only, triage of every finding, fixes checked against the inventory, stop rules.
---

# Cold review loop

A builder that checks its own document reads its intentions, not the page. This skill puts every finished document in front of a reader who has seen none of the work, in rounds, until it is clean.

Run it after `cv-build-from-jd` and `second-pass-rubric`, never before. A reviewer's time is wasted on a draft the builder has not checked.

## Prepare the round

1. Check the document for banned phrases, repeated numbers and sentences without verbs: run `scripts/check_document.py` if the repository's scripts are available to you, or check by reading.
2. Export the document to plain text, with `scripts/export_cv_text.py` or by saving it as text.
3. Save the job description as a text file beside it. A folder called `review/` keeps each round's files together.
4. Make sure the style guide you give the reviewer holds writing rules only. Personal facts belong in the project context, which the reviewer never sees.
5. Open a triage log for this document from `references/triage_log.md`.

## Run the reviewer

Start a new reviewer for every round. Give it the brief in `references/reviewer_brief.md` with three paths filled in: the job description, the CV text and the style guide. Give it nothing else: no inventory, no cast list, no conversation, no earlier report.

In Claude Code, hand the brief to the `cold-reviewer` subagent. From a terminal, run `bash scripts/review_round.sh`. In Claude.ai, paste the brief into a new chat outside the Project, attach the three files, and replace the three paths in the brief with the names of the attached files.

## Triage every finding

Record each finding in the triage log as accept, reject or ask.

- **Accept** when the finding is right and the fix needs no new fact. Check every accepted change against the inventory before making it.
- **Reject** when the finding conflicts with the person's standing rulings or with a fact the reviewer could not see. Write the reason.
- **Ask** when the fix needs a fact the archive does not hold. The finding becomes a question for the person.

Rules:

- A reviewer never adds a fact. A fix that needs a new claim is a question.
- The person's rulings outrank any reviewer on length, disclosure and silence.
- Fix style faults with the plainest sentence, never with a different device. Fronting the object or switching to the passive to avoid a run of "I" is a new fault, not a fix.
- When two reviewers who never saw each other's reports flag the same line, treat it as settled unless the person rules otherwise.
- Keep everything the reviewer lists under KEEP unless the person rules otherwise.

## Apply and repeat

Apply the accepted changes. Re-run the checker. Export again. Start a new reviewer for the next round.

Stop when a round returns no high or medium finding that the builder can fix from the archive, or after three rounds. After the person answers the remaining questions, run one final round.

## Report to the person

Deliver the document. Then give, in this order: the verdict and score from each round; what changed, in a few lines; what was rejected and why, if the person would want to know; and the questions, numbered, each with the finding that raised it. When the answers come back, bank them in the inventory the same day with `receipts-inventory`, apply them, and run the final round.
