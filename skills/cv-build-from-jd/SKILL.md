---
name: cv-build-from-jd
description: Build or retune a CV for a job description: assess fit, choose the base, write the profile and blocks, place receipts, judge credentials, knife, hand off.
---

# CV build from a job description

Obey `prose-law` throughout. Read it in full first.

## 1. Assess before building

Read the whole posting. Map every requirement to a receipt in the inventory or to a gap. Then tell the person, in this order and plainly: the fit; the level against their target; compensation with the reasoning in one line; the odds as an over/under; the one or two filters that decide it; and what would make it the wrong seat. Wait for the decision. Build only on the word. Assessment is honest even when the person will build anyway.

## 2. Choose the base

Keep a small number of knifed base documents, one per funnel: customer-facing seats, technology-leadership seats, services and consultancy seats, founder-side seats, practitioner or interim seats. Copy the nearest base. Never build from the master document directly; the master is a quarry, and quarries have everything in them twice.

## 3. Write the profile

Two paragraphs, three at most. Open on the largest true claim for this seat, not the earliest. Order by weight. Every sentence is a receipt with a number or a name attached, or a plain statement of scope. The profile carries the headline figures and carries each exactly once. It never announces what the person is; the reader derives that. Nothing in it is chronology for its own sake, nothing is a habit-claim ("I always…"), nothing is a device from the banned families, and nothing is a phrase borrowed from the posting.

If the person has stated the thesis for this candidacy in their own words, build down from that sentence. Building down from a stated claim beats building up from the archive every time it has been tried.

## 4. Retune the capability blocks

Four blocks, lowercase, each a list of things the person has done, in the vocabulary a screener for this seat will search. No numbers in blocks. No sentences. No coinages or workshop phrases; name the practice by its public name.

## 5. Place receipts in the career cells

Each role gets bullets at one theme per bullet, so a thirty-second skim finds the evidence. The operational figures live here, once each, and never in the profile as well. Lift the receipts most relevant to this seat toward the top of each cell. If a fact belongs to the whole tenure, put it in the cell where it happened, not where it sounds best.

## 6. Judge the certifications for this reader

Consult the person's per-credential rulings. Technician badges on a technician document; executive documents carry only credentials that support a claim the document makes; a professional chartership goes in the header. When the posting names a certification the person holds, put it first.

## 7. Knife pass

Cut, in this order: anything irrelevant to this reader; anything the reader would have to look up (internal project names, house jargon) unless it anchors a checkable fact; decorative facings that describe the shape of a role rather than its content; name-drops; anything that reads as recent-context leakage; technician detail on an executive page; volunteer credentials dressed as domain experience; every device in the banned families; every number told twice.

## 8. Check, then hand off

Render the document and check the page count. Sweep for banned phrases and repeated numbers with `scripts/check_document.py`. Then run `second-pass-rubric`. A first build is a draft until the second pass has run and the embarrassment test has been applied.

## Working with Word documents

Use `scripts/docx_helpers.py`: `set_text` replaces a paragraph's text while keeping its formatting; `set_block` rewrites a bold-label capability block; `set_bullets` rewrites a cell's bullet list; `cells` walks nested tables. Render with LibreOffice headless to a PDF for page count and a page-one image for a visual check before presenting.
