import re


def chunk_text(text, chunk_size=800, overlap_sentences=1):
    text = re.sub(r"\s+", " ", text)
    sentences = re.split(r"(?<=[.!?])\s+", text)

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