"""Check a Word document for banned devices, repeated numbers, verbless sentences and length.

Usage: python check_document.py path/to/document.docx

Reports banned phrases (a starter list; extend BANNED with your own rulings), em dashes,
sentences with no finite verb in the profile and the role entries, numbers that appear more
than once, and the page count if LibreOffice (soffice) and pdfinfo are on the path.

Repeated numbers are advisory: a number may appear twice when the plain sentence needs it.
The verb check is a heuristic that looks for a common verb form; read what it flags.
Exit code is 1 if a banned phrase or a verbless sentence is found.
"""
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from docx import Document

BANNED = [
    # "under" in any sense other than physically beneath or below a number
    r"\bunder (?:a |the |my |its |our |their |his |her )?(?:governance|controls?|standards?|accountability|leadership|policy|policies|review|audit|management|supervision|oversight)\b",
    # antithesis and fronted noun phrases
    r"\bnot [a-z ]{1,30} but\b", r"\brather than\b", r"\bis (?:what|how|where|the one|the thing) I\b",
    # assistant vocabulary and self-certifying adjectives
    r"\bgenuinely\b", r"\bleverag", r"\bseamless", r"\brobust\b", r"\bpassionate\b", r"\bjourney\b",
    r"\badjacen", r"\becosystem\b", r"\bproven\b", r"\bworld-class\b", r"\bexceptional\b",
    r"\b(?:both|other) sides? of the table\b",
    # absolute constructions
    r"\bhaving [a-z]+ed\b",
    # mannered prose
    r"\bearns its (?:place|keep)\b", r"\bhome ground\b", r"\bdoes the (?:heavy lifting|work)\b",
    r"\b(?:strong|trump|wild|calling) card\b", r"\bcards? (?:to play|on the table)\b",
    # commute logistics
    r"\b(?:ten|fifteen|twenty|thirty|forty|fifty|sixty) minutes from\b", r"\ban hour from\b",
    # em dashes
    r"—",
]

# Common finite verb forms. Extend it if the check flags sentences that do have a verb.
VERB_HINT = re.compile(
    r"\b(?:am|is|are|was|were|be|been|being|has|have|had|do|does|did|will|would|can|could|should|may|might|must|shall"
    r"|ran|run|runs|built|builds?|wrote|writes?|led|leads?|owned|owns?|set|sets|created|creates?|took|takes?|held|holds?"
    r"|made|makes?|grew|grows?|moved|moves?|put|kept|keeps?|went|goes|came|comes?|said|says?|gave|gives?|got|gets?"
    r"|saw|sees?|sat|left|found|brought|brings?|cut|cuts|paid|pays?|won|wins?|lost|met|taught|told|felt|began|spent|stood"
    r"|worked|works?|served?|serves|reported|reports?|delivered|delivers?|managed|manages?|designed|designs?|replaced|replaces?"
    r"|exited|retired|carried|carries|trained|trains?|chaired|chairs?|founded|applied|joined|opened|closed|turned|asked"
    r"|started|hired|coached|reviewed|reviews?|passed|supported|supports?|handled|diagnosed|diagnoses|lives?|lived"
    r"|speaks?|spoke|completed|use[ds]?|uses|steered|steers?|selected|selects?|reached|reaches|earned|learned|settled"
    r"|agreed|decided|showed|shows?|predicted|predicts?|briefed|advised|fell|falls?|rose|rises?|dropped|drafted|drafts?"
    r"|estimated|shipped|needed|needs?|called|helped|helps?|existed|exists?|counted|arrived|filtered|raised|measured"
    r"|measures?|reduced|reduces?|prioritised|represented|knows?|knew|explained|audited|fed|scaled|influenced|documented"
    r"|presented|queried|sold|sells?|drew|checked|checks?|judged|caught|appeared|planned|absorbed|forecast|includes?|included"
    r"|covers?|covered|means|meant|instituted|oversaw|negotiated|executed|appointed|restored|promoted|redesigned|consolidated"
    r"|routes?|routed|relied|relies|rely|stayed|stays?|let|lets|flagged|flags?|added|adds?|removed|removes?|resolved|resolves?|cleared|ended|ends?|grew|launched|migrated|integrated|automated|tracked|tested|wanted|offered|became|becomes?|remained|remains?|continued)\b",
    re.I,
)


def walk_cells(container):
    """Yield every table cell, including cells of tables nested inside cells."""
    for table in container.tables:
        for row in table.rows:
            for cell in row.cells:
                yield cell
                yield from walk_cells(cell)


def all_paragraphs(doc):
    paragraphs = list(doc.paragraphs)
    for cell in walk_cells(doc):
        paragraphs.extend(cell.paragraphs)
    return paragraphs


def repeated_numbers(text):
    numbers = re.findall(r"(?<![\w.])(?:[$£€]\s?)?\d[\d,]*(?:\.\d+)?(?:%|m|k|bn)?", text)
    numbers = [n.strip() for n in numbers if len(re.sub(r"\D", "", n)) >= 2]
    # Years and the 24 in "24/7" are dates and idioms, not figures.
    numbers = [n for n in numbers if not re.fullmatch(r"(?:19|20)\d\d", n) and n != "24"]
    # Product names that contain numbers (Microsoft 365, ISO 27001) are names, not figures.
    for name in re.findall(r"(?:Office|Microsoft|ISO|Windows)\s?(\d+)", text):
        while name in numbers:
            numbers.remove(name)
    counts = Counter(numbers)
    return {n: c for n, c in counts.items() if c > 1}


def no_verb_sentences(paragraphs):
    """Sentences of six words or more in which no common verb form appears."""
    hits = []
    for paragraph in paragraphs:
        text = paragraph.text.strip()
        # Skip short lines, Stack lines, header lines ("Title | Company | Dates") and headings without a full stop.
        if len(text) < 60 or text.startswith("Stack:") or " | " in text or not text.endswith((".", "!", "?")):
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            words = sentence.strip()
            if len(words.split()) >= 6 and not VERB_HINT.search(words) and not words.endswith(":"):
                hits.append(words[:90])
    return hits


def structure_problems(path):
    """Faults Word reports as a corrupt file: a table cell that does not end in a paragraph,
    duplicate or unbalanced bookmarks, and duplicate paragraph ids (all common after copying rows)."""
    import zipfile
    from lxml import etree
    w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    w14 = "{http://schemas.microsoft.com/office/word/2010/wordml}"
    root = etree.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    problems = []
    empty = sum(1 for tc in root.iter(w + "tc") if not [k for k in tc if k.tag != w + "tcPr"] or [k for k in tc if k.tag != w + "tcPr"][-1].tag != w + "p")
    if empty:
        problems.append(f"{empty} table cell(s) not ending in a paragraph")
    starts = [b.get(w + "id") for b in root.iter(w + "bookmarkStart")]
    ends = {b.get(w + "id") for b in root.iter(w + "bookmarkEnd")}
    if len(starts) != len(set(starts)) or set(starts) != ends:
        problems.append("duplicate or unbalanced bookmarks")
    ids = [p.get(w14 + "paraId") for p in root.iter(w + "p") if p.get(w14 + "paraId")]
    if len(ids) != len(set(ids)):
        problems.append("duplicate paragraph ids")
    return problems


def page_count(path):
    try:
        out = tempfile.mkdtemp()
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", out, path],
                       check=True, capture_output=True, timeout=120)
        pdf = Path(out) / (Path(path).stem + ".pdf")
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        match = re.search(r"Pages:\s+(\d+)", info)
        return int(match.group(1)) if match else None
    except Exception:
        return None


def main(path):
    doc = Document(path)
    paragraphs = all_paragraphs(doc)
    text = "\n".join(p.text for p in paragraphs)
    found = False
    for pattern in BANNED:
        for match in re.finditer(pattern, text, flags=re.I):
            found = True
            start = max(0, match.start() - 40)
            print(f"BANNED  {pattern!s:40} … {text[start:match.end() + 40].replace(chr(10), ' ')}")
    for sentence in no_verb_sentences(paragraphs):
        found = True
        print(f"NOVERB  {sentence}")
    for number, count in sorted(repeated_numbers(text).items(), key=lambda x: -x[1]):
        print(f"REPEAT  {number} appears {count} times (advisory)")
    for problem in structure_problems(path):
        found = True
        print(f"CORRUPT {problem} (Word may refuse to open the file)")
    pages = page_count(path)
    if pages is not None:
        print(f"PAGES   {pages}")
    return 1 if found else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
