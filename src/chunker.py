import re


def chunk_text(text, chunk_size=800, overlap_sentences=1):
    text = re.sub(r"\s+", " ", text)
    sentences = re.split(r"(?<=[.!?;:—])\s+", text)

    chunks, current, length = [], [], 0
    for sentence in sentences:
        if length + len(sentence) > chunk_size and current:
            chunks.append(" ".join(current))
            current = current[-overlap_sentences:] if overlap_sentences else []
            length = sum(len(s) for s in current)
        current.append(sentence)
        length += len(sentence)

    if current:
        chunks.append(" ".join(current))
    return chunks


def chunk_section(title, section, text, chunk_size=1200):
    """One chunk per section if it fits. Long sections are split, and every
    piece starts with 'Title, Section N' so it makes sense on its own."""
    header = f"{title}, Section {section}" if section != "preamble" else f"{title}, Preamble"
    if len(text) <= chunk_size:
        return [f"{header}: {text}"]
    return [f"{header} (part {i}): {p}" for i, p in enumerate(chunk_text(text, chunk_size), 1)]