import re

LIGATURES = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl"}

# Running page headers of the Gazette of India. Scanned copies add OCR typos
# (GAZETTER, iNDIA, "SEC.1"), so the match is case-insensitive and tolerant.
HEADER_RE = re.compile(
    r"(?:SEC\.?\s*\d*\]?\s*)?THE\s+GAZETTER?\s+OF\s+INDIA\s+EXTRAORDINARY"
    r"(?:\s*\[P\s*ART\s*II\s*[—-](?:\s*SEC\.?\s*\d*\])?)?(?:[ \t]*\d{1,3}\b)?",
    re.IGNORECASE,
)
PAGENUM_BEFORE_HEADER_RE = re.compile(
    r"(?m)^\d{1,3}\s+(?=THE\s+GAZETTER?\s+OF)|(?<=[;.,:\w])\d{1,3}\s+(?=THE\s+GAZETTER?\s+OF)",
    re.IGNORECASE,
)


def clean_text(text):
    for bad, good in LIGATURES.items():
        text = text.replace(bad, good)
    text = text.replace("\u00a0", " ")
    text = PAGENUM_BEFORE_HEADER_RE.sub("", text)
    text = HEADER_RE.sub("", text)
    # Consolidated Acts mark amendments as 2[...text...]; drop the markers, keep the text.
    text = re.sub(r"(?<![\w.])\d{1,2}\[", "", text)
    text = text.replace("[", "").replace("]", "")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()