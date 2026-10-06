# Style guide: [your name]

Your private style guide is the prose law plus your own writing rulings. The assistant reads this whole file before every build, and the cold reviewer reads it too, so it holds writing rules only. Facts about you (where you live, availability, anything confidential) go in `Project_Context.md`, which the reviewer never sees.

## The prose law

Paste here the body of `skills/prose-law/SKILL.md`, everything below its frontmatter (the block between the two `---` lines at the top).

## My rulings

Add one entry each time you correct the assistant's writing. Date it, quote the offending phrase, say what to write instead, and say whether the checker should catch it.

- [Date]. "[Phrase the assistant wrote]" is banned. Write "[what you would say]". Added to the checker: [yes/no].

## Words and phrases I never want to see

- [word or phrase]

## Repeat offences

When a banned device returns, note the date and the document. Patterns here show which rules belong in `scripts/check_document.py`.
