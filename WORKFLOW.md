# The workflow: build, review cold, triage, repeat

An assistant that writes a document and then checks it is marking its own homework. It has read the archive, so it fills gaps from memory that the page does not hold. It made the choices, so it reads them as intended. And its habits, the ones the prose law bans, look normal to it because they are its own.

The cure is a second reader who has seen none of the work. Second runs every document through rounds of review by fresh agents, each with minimal context, until the document is clean or the remaining problems need facts only the person holds.

## The cast

| Role | Who | Sees | Does |
|---|---|---|---|
| The person | You | Everything | Decides, supplies facts, rules on disputes. |
| The builder | Your main Claude session | The archive, the job description, the conversation | Builds, triages, edits, asks, banks new facts. |
| The reviewer | A fresh agent, new every round | Three files: the job description, the CV as plain text, the style guide | Reads as the hiring reader and as the style auditor. Reports. Never edits. |
| Parallel builders (optional) | Subagents, one per posting | The archive and one job description | Produce first drafts during a wave. |

The reviewer never sees the inventory, the cast list, the project context or the conversation. That is the point. It reads the way a stranger reads.

## One build, start to finish

```
 job description
       │
       ▼
 ┌─────────────┐   protocol: JD in full → inventory in full → build from scratch
 │   BUILD     │   → prose law → second pass → check_document.py → export to text
 └─────┬───────┘
       ▼
 ┌─────────────┐   fresh reviewer, three files only
 │  REVIEW n   │   verdict · numbered findings · three things to keep
 └─────┬───────┘
       ▼
 ┌─────────────┐   accept · reject with reason · ask the person
 │   TRIAGE    │   every accepted change checked against the inventory
 └─────┬───────┘
       ▼
 ┌─────────────┐   edit, re-run the checker, re-export
 │    APPLY    │
 └─────┬───────┘
       ▼
  any high or medium finding left that the builder can fix, and fewer than 3 rounds run?
       │ yes → REVIEW n+1 (a new reviewer)
       │ no
       ▼
  deliver the document + a short list of questions for the person
       │
       ▼
  person answers → bank the answers → apply → one final review round
```

### Step 1: build

Follow `skills/cv-build-from-jd` in order. Read the job description in full and list its requirements. Read the whole inventory, weighted by relevance and not by recency. Build from scratch, with the evidence in the role entries and a short profile that summarises them. Run the prose law, then the checker, then the second-pass rubric:

```
python scripts/check_document.py CV.docx
```

Then save the job description and a plain-text export of the CV in a `review/` folder for the reviewer:

```
mkdir -p review
# paste the job description into review/JD.txt
python scripts/export_cv_text.py CV.docx > review/CV_round1.txt
```

The style guide you give the reviewer should hold writing rules only. Keep personal facts (where you live, your availability, anything confidential) in the project context, which the reviewer never sees.

### Step 2: review

Start a new reviewer for every round. Give it the brief in `skills/cold-review-loop/references/reviewer_brief.md` with three paths filled in. Nothing else. Three ways to run it are below, under "Running the reviewer".

The reviewer returns a verdict (shortlist or not, a score out of ten, one sentence of reason), up to twenty findings ranked by severity, and the three strongest things in the document.

### Step 3: triage

The builder takes every finding in turn and records one of three outcomes in the triage log (`skills/cold-review-loop/references/triage_log.md`):

- **Accept.** The finding is right and the builder can fix it from the archive. Check the change against the inventory before making it.
- **Reject, with a reason.** The finding conflicts with the person's standing rulings, or with a fact the reviewer could not see. Write the reason down, so a later round that raises it again is answered in a line.
- **Ask.** The finding is right, but the fix needs a fact the archive does not hold: a number, a scope, a name. It goes on the list of questions for the person.

Five rules govern triage.

1. **A reviewer never adds a fact.** If a finding can only be fixed by claiming something new, it becomes a question, never an edit.
2. **The person's rulings outrank any reviewer** on length, on what is disclosed and on what is left unsaid.
3. **Do not fix a style finding with a different device.** A run of sentences starting with "I" is not cured by fronting the object ("the budget was mine") or by turning the sentence passive. Both are faults of their own. Write the plainest subject-verb-object sentence, and join two short ones with "and" when they belong together.
4. **Agreement between rounds is a signal.** When two reviewers who never saw each other's reports flag the same line, treat the finding as correct, unless the person has ruled on that line.
5. **Keep what the reviewer says to keep.** The KEEP list protects the strongest material from later edits, unless the person rules otherwise.

### Step 4: apply and repeat

Make the accepted changes, re-run the checker, export again, and start a new reviewer. A reviewer that has seen round one will defend its own suggestions in round two, so it is never reused.

Stop when a round returns no high or medium finding that the builder can fix from the archive, or after three rounds. After the person answers the remaining questions, run one final round. Deliver the document with the questions. When the person answers, bank the answers in the inventory the same day, apply them, and run that final round. If the final round still finds something serious, it goes to the person as a last short list; the document is not held back for further rounds unless the person asks.

## Running the reviewer

### In Claude Code, as a subagent

Copy `.claude/agents/cold-reviewer.md` into your project's `.claude/agents/`. A subagent starts with a fresh context and does not receive the main conversation. This one has only the Read tool and is set not to load `CLAUDE.md`. It can still read any file in the project if told to, so the isolation rests on its instructions and on the builder passing it only three paths. For isolation that does not depend on instructions, use the command-line route below, which copies the three files into an empty folder. Ask the builder:

```
Run the cold-reviewer on review/JD.txt, review/CV_round1.txt and archive/Style_Guide.md.
```

The builder fills in the brief and hands it over. The report comes back to the builder, which triages it.

### From the command line

`scripts/review_round.sh` copies the three files into an empty temporary folder and runs Claude Code headless there, with a permission mode that denies anything needing approval. Reads inside that folder are allowed, and everything else is refused, so the reviewer cannot wander into your archive:

```
bash scripts/review_round.sh review/JD.txt review/CV_round1.txt archive/Style_Guide.md > review/report_round1.md
```

An optional fourth argument describes the reader, for example `"a recruitment consultant, and behind them the hiring manager"`.

If `ANTHROPIC_API_KEY` is set, the script adds `--bare`, which also skips your personal `CLAUDE.md`, skills, hooks and plugins. Without an API key, it runs with your normal login, and anything in `~/.claude/CLAUDE.md` will load. Keep personal facts out of that file if you use this route.

### In Claude.ai

Open a new chat outside the Project that holds your archive. Paste the brief, attach the three files, replace the three paths in the brief with the names of the attachments, and send. Copy the report back into the Project chat for triage. Use a new chat for every round.

## A wave of postings

When several job descriptions arrive at once, the first drafts can be built in parallel. In Claude Code, the builder hands each posting to a subagent with access to the archive and the instruction to follow `skills/cv-build-from-jd` and stop at a first draft. Three rules apply:

- Each parallel builder reads the full prose law and the full inventory itself. A summary in the hand-off is not enough, because the law does not survive summarising.
- Only the main session writes to the inventory. Parallel builders list new facts and questions in their report; the builder banks them, so two agents never edit the same file.
- The main session does the prose pass and the triage on every draft. Each draft then gets its own cold review rounds.

Use the session's task list, if it has one, with one task per posting and stage, so a person who steps away can see what is done.

## What reviewers are good at, and what they are not

From practice:

- **Good:** requirements the document never answers with an instance; claims larger than their evidence; a profile and a role entry that disagree; jargon a reader in another sector would have to look up; style faults the builder has stopped seeing; lines that read as forced fit for this reader.
- **Not good:** knowing what is true. A reviewer cannot tell a modest truth from an inflation, and it will sometimes push to add experience. The brief forbids it, and triage catches it.
- **Mixed:** consistency with the person's own settled rulings. A reviewer will flag a choice the person made on purpose. Record the ruling as the reason for rejection, and move on.

Expect each round to take a few minutes. Two rounds usually take a document from a first build to one a careful stranger would put forward, and leave a short list of questions that only the person can answer. Those questions are often worth more than the edits.
