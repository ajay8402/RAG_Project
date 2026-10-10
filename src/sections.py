import re

SECTION_RE = re.compile(r"^(\d{1,3})([A-Z]{0,2})\.\s+(?=[(\"“‘A-Z])")
CHAPTER_RE = re.compile(r"^CHAPTER\s+([IVXL]+)\s*$")


def _is_next(num, suffix, last_num, last_suffix):
    """Accept only the section that should come next (35 after 34, or 194D after 194C)."""
    if num == last_num + 1:
        return suffix == ""
    if num == last_num and suffix and suffix > last_suffix:
        return True
    return False


def split_sections(pages):
    """Split a legal document (list of page texts) into sections.

    A line starting with a number counts as a new section only if it is the
    next expected number, which filters out numbered lists and page numbers.
    """
    sections = []
    current = {"section": "preamble", "chapter": "", "page": 1, "lines": []}
    last_num, last_suffix = 0, ""
    chapter = ""

    for page_no, page_text in enumerate(pages, start=1):
        for line in page_text.split("\n"):
            stripped = line.strip()
            if not stripped:
                continue

            m = CHAPTER_RE.match(stripped)
            if m:
                chapter = m.group(1)

            m = SECTION_RE.match(stripped)
            if m and _is_next(int(m.group(1)), m.group(2), last_num, last_suffix):
                sections.append(current)
                last_num, last_suffix = int(m.group(1)), m.group(2)
                current = {
                    "section": f"{last_num}{last_suffix}",
                    "chapter": chapter,
                    "page": page_no,
                    "lines": [],
                }
            current["lines"].append(stripped)

    sections.append(current)
    return [
        {
            "section": s["section"],
            "chapter": s["chapter"],
            "page": s["page"],
            "text": " ".join(s["lines"]),
        }
        for s in sections
        if s["lines"]
    ]