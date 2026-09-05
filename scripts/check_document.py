"""Check a Word document for banned devices, repeated numbers and length.

Usage: python check_document.py path/to/document.docx

Reports: banned phrases (a starter list; extend it with the person's own bans),
numbers that appear more than once, em dashes, and the page count if LibreOffice
is available on the path. Exit code is 1 if anything is found.
"""
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from docx import Document

BANNED = [
    r"\bnot [a-z ]{1,30} but\b", r"\brather than\b", r"\bgenuinely\b", r"\bleverag", r"\bseamless",
    r"\brobust\b", r"\bpassionate\b", r"\bjourney\b", r"\badjacen", r"\becosystem\b", r"\bproven\b",
    r"\bworld-class\b", r"\bexceptional\b", r"\bhaving [a-z]+ed\b", r"—",
    r"\b(?:twenty|thirty|forty|fifty|sixty) minutes from\b", r"\ban hour from\b",
    r"\bis (?:what|how|where|the one|the thing) I\b", r"\bearns its (?:place|keep)\b",
    r"\bhome ground\b", r"\bdoes the work\b",
]


def all_text(doc):
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                parts.extend(p.text for p in cell.paragraphs)
    return "\n".join(parts)


def repeated_numbers(text):
    numbers = re.findall(r"(?<![\w.])(?:[$£€]\s?)?\d[\d,]*(?:\.\d+)?(?:%|m|k|bn)?", text)
    numbers = [n.strip() for n in numbers if len(re.sub(r"\D", "", n)) >= 2]
    # Years and the 24 in "24/7" are dates and idioms, not receipts; ignore them.
    numbers = [n for n in numbers if not re.fullmatch(r"(?:19|20)\d\d", n) and n != "24"]
    counts = Counter(numbers)
    return {n: c for n, c in counts.items() if c > 1}


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
    text = all_text(doc)
    found = False
    for pattern in BANNED:
        for match in re.finditer(pattern, text, flags=re.I):
            found = True
            start = max(0, match.start() - 40)
            print(f"BANNED  {pattern!s:40} … {text[start:match.end() + 40].replace(chr(10), ' ')}")
    for number, count in sorted(repeated_numbers(text).items(), key=lambda x: -x[1]):
        found = True
        print(f"REPEAT  {number} appears {count} times")
    pages = page_count(path)
    if pages is not None:
        print(f"PAGES   {pages}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
