from src.loader import load_documents
from src.chunker import chunk_text
from src.vectorstore import add_chunks, search

docs = load_documents()
print(f"Loaded {len(docs)} documents")

for doc in docs:
    chunks = chunk_text(doc["text"])
    add_chunks(doc["source"], chunks)
    print(f"Stored {len(chunks)} chunks from {doc['source']}")

query = "What is deep learning?"
print(f"\nQuestion: {query}\n")
for i, result in enumerate(search(query), 1):
    print(f"--- Result {i} ---")
    print(result)
    print()