import re

# A section starts with its number. Real Acts decorate it in different ways:
#   "2[2A. E-cart..."       amendment marker before the number
#   "Appeal 19. (1) ..."    side heading on the same line (scanned copies)
#   "93. 2[Agent or ...]"   amendment marker before the heading
SECTION_RE = re.compile(
    r"^(?:\d{1,3}\s*\[+\s*|\[+\s*)?"
    r"(?:(?P<lead>[A-Z][^\d]{0,60}?)\s)?"
    r"(?P<num>\d{1,3})(?P<suf>[A-Z]{0,2})\.\s*"
    r"(?=(?:\d{1,3}\[)?[(\"“‘\[A-Z])"
    r"(?!(?:Subs|Ins|Added|Rep|Renumbered|Re-numbered|Substituted|Inserted|Cl|Clause|Ibid)\b)"
)
LEAD_BAD_END_RE = re.compile(r"(?i)\b(section|sections|sub-section|clause|and|or|of|to|in|under)$")
CHAPTER_RE = re.compile(r"^CHAPTER\s+([IVXL]+)\s*$")
SCHEDULE_RE = re.compile(r"^(?:THE\s+)?(FIRST|SECOND|THIRD|FOURTH)\s+SCHEDULE\b", re.IGNORECASE)


def _is_next(num, suffix, last_num, last_suffix):
    """Accept only the section that should come next (35 after 34, or 194D after 194C)."""
    if num == last_num + 1:
        return suffix == ""
    if num == last_num and suffix and suffix > last_suffix:
        return True
    return False


def _looks_like_toc(sections, current):
    """True if the sections collected so far are one-line table-of-contents entries."""
    sizes = sorted(
        len(" ".join(x["lines"])) for x in sections + [current] if x["section"] != "preamble"
    )
    return len(sizes) >= 5 and sizes[len(sizes) // 2] < 200


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

            sm = SCHEDULE_RE.match(stripped)
            if sm:
                # A schedule is its own part of the Act, not the tail of the last section.
                sections.append(current)
                current = {
                    "section": f"{sm.group(1).title()} Schedule",
                    "chapter": "",
                    "page": page_no,
                    "lines": [stripped],
                }
                continue

            m = SECTION_RE.match(stripped)
            if m and m.group("lead") and LEAD_BAD_END_RE.search(m.group("lead")):
                m = None  # the text before the number is a cross-reference like "under section 19."

            if (m and int(m.group("num")) == 1 and not m.group("suf") and last_num >= 5
                    and _looks_like_toc(sections, current)):
                # "1." appeared again after a run of one-line entries: that was the
                # table of contents ("Arrangement of Sections"), so start over.
                sections = []
                current = {"section": "preamble", "chapter": "", "page": page_no, "lines": []}
                last_num, last_suffix = 0, ""

            if m and _is_next(int(m.group("num")), m.group("suf"), last_num, last_suffix):
                sections.append(current)
                last_num, last_suffix = int(m.group("num")), m.group("suf")
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