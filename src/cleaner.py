import re

LIGATURES = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl"}

# Running page headers printed by the Gazette of India
HEADER_RE = re.compile(
    r"(?:SEC\.\s*\d+\]\s*)?THE GAZETTE OF INDIA EXTRAORDINARY"
    r"(?:\s*\[P\s*ART\s*II—(?:\s*SEC\.\s*\d+\])?)?(?:[ \t]*\d{1,3}\b)?"
)
PAGENUM_BEFORE_HEADER_RE = re.compile(
    r"(?m)^\d{1,3}\s+(?=THE GAZETTE OF INDIA)|(?<=[;.,:\w])\d{1,3}\s+(?=THE GAZETTE OF INDIA)"
)


def clean_text(text):
    for bad, good in LIGATURES.items():
        text = text.replace(bad, good)
    text = text.replace("\u00a0", " ")
    text = PAGENUM_BEFORE_HEADER_RE.sub("", text)
    text = HEADER_RE.sub("", text)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()