from src.loader import load_documents
from src.chunker import chunk_text

docs = load_documents()
print(f"Loaded {len(docs)} documents")

for doc in docs:
    chunks = chunk_text(doc["text"])
    print(f"{doc['source']} -> {len(chunks)} chunks")
    print("First chunk preview:", chunks[0][:150] if chunks else "(empty)")