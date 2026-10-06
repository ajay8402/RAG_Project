from src.loader import load_documents
from src.chunker import chunk_text
from src.vectorstore import add_chunks, reset

reset()
for doc in load_documents():
    chunks = chunk_text(doc["text"])
    add_chunks(doc["source"], chunks)
    print(f"Stored {len(chunks)} chunks from {doc['source']}")