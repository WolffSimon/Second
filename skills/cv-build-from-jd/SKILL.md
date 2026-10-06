---
name: cv-build-from-jd
description: Build a CV for one job description in protocol order: assess, read the inventory, build from scratch, prose law, second pass, then cold review rounds.
---

# CV build from a job description

Obey `prose-law` throughout. Read it in full first.

## The protocol, in order

1. Read the job description in full and list its requirements.
2. Read the whole inventory, weighted by relevance and not by recency, and mark the receipts that answer each requirement.
3. Build from scratch, not by retuning the last document. The evidence goes into the role entries, against the jobs where it happened. The profile is two short paragraphs that summarise what the entries prove.
4. Run the prose law on the whole document.
5. Run `second-pass-rubric`.
6. Run `cold-review-loop`.

A document that skips a step is a draft. The sections below walk through the protocol: section 1 covers steps 1 and 2, sections 2 to 7 cover steps 3 and 4, and section 8 covers steps 5 and 6.

## 1. Assess before building

Map every requirement to a receipt in the inventory or to a gap. Then tell the person, plainly and in this order: the fit; the level against their target; pay, with the reasoning in one line; the chances, as a rough percentage with the reasoning; the one or two filters that will decide it; and what would make it the wrong seat. Wait for the decision. Build only when the person says so. Assessment is honest even when the person will build anyway.

## 2. Choose the shell, not the content

Keep a small number of rated base documents, one for each family of role you apply for (by function, by level, or by permanent and interim). A rated base is a CV that has been through review and that the person is content with. Copy the nearest base for its layout and its header, education and early-career sections. Write the profile and the role entries fresh for this posting. Start from the most recently rated document of the family, never from the most recently edited one: a document that has been patched four times is a draft again.

## 3. Write the profile

Two paragraphs. Open on the largest true claim for this seat, not the earliest. If the reader will not recognise the employers, one plain descriptor sentence may come first (see `prose-law`). Every sentence after it is a receipt with a number or a name attached, or a plain statement of scope. Nothing in it is chronology for its own sake, a habit-claim ("I always…"), a device from the banned families, or a phrase borrowed from the posting. Degrees and certificates belong in the education section, not the profile.

If the person has stated the case for this candidacy in their own words, build down from that sentence. Building down from a stated claim beats building up from the archive every time.

See `references/profile_patterns.md` for three shapes.

## 4. Write the role entries

Each role gets entries in prose, one theme per entry, so a thirty-second skim finds the evidence. Every sentence has a subject and a finite verb. The operational figures live here. Lift the receipts most relevant to this seat to the top of each role. A fact that belongs to a particular era goes in the role where it happened, not where it sounds best. On technical seats, end each role with a Stack line of tools from the inventory; on seats the posting calls non-technical, keep it short or leave it off.

Current part-time or fractional roles and ventures each get their own entry, with an honest title.

## 5. Capability blocks, only where a machine reads first

Keyword blocks under the profile help where an applicant-tracking system and a recruiter's scan come before any human reading. Cut them where someone who knows the person will pass the document straight to the hiring manager, or where the employer says a person reads every application. Where they stay: four at most, capability names only, no numbers, no names, no sentences, no participles ("Teams Built" is signage, not a capability).

## 6. Judge the certifications for this reader

Consult the person's per-credential rulings. Technician badges go on technician documents. Executive documents carry only credentials that support a claim the document makes. A professional chartership goes in the education section or the header. When the posting names a certification the person holds, put it first.

## 7. Knife pass

Cut, in this order: anything irrelevant to this reader; anything the reader would have to look up (internal project names, house jargon) unless it anchors a checkable fact; decorative capability nouns that name nothing checkable; adviser and celebrity name-drops (client names are receipts and stay); anything imported from the last posting you read; technician detail on an executive page; volunteer credentials dressed as domain experience; every device in the banned families.

## 8. Check, then hand off to review

Render the document and check the page count. If the scripts in this repository are available to you (in Claude Code, or on your own machine), run `scripts/check_document.py` for banned phrases, repeated numbers, sentences without verbs and length; otherwise make the same checks by reading. Run `second-pass-rubric`. Then export the document to text (`scripts/export_cv_text.py`, or save it as plain text) and run `cold-review-loop`.

## Working with Word documents

`scripts/docx_helpers.py` gives `set_text` (replace a paragraph's text and keep its formatting), `set_block` (rewrite a bold-label keyword block), `set_bullets` (rewrite a cell's list of entries to exactly the texts given) and `cells` (walk nested tables). `scripts/italicise_stacks.py` sets Stack lines in italics. `scripts/add_education_tools.py` adds a tools line under named education entries from a small JSON file. Render with LibreOffice headless to a PDF for the page count and a page-one image for a visual check before presenting.
