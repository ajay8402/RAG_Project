from pathlib import Path

from src.loader import load_documents
from src.chunker import chunk_section
from src.sections import split_sections
from src.vectorstore import add_chunks, reset

reset()
for doc in load_documents():
    title = Path(doc["source"]).stem.replace("_", " ").title()
    total = 0
    for sec in split_sections(doc["pages"]):
        chunks = chunk_section(title, sec["section"], sec["text"])
        add_chunks(
            doc["source"], chunks,
            page=sec["page"], section=sec["section"], chapter=sec["chapter"],
        )
        total += len(chunks)
    print(f"Stored {total} chunks from {doc['source']}")