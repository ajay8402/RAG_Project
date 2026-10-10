from src.vectorstore import search
from src.generator import answer

print("Ask questions about your document. Type 'exit' to quit.")

while True:
    question = input("\nYou: ").strip()
    if question.lower() in ("exit", "quit"):
        break
    if not question:
        continue

    chunks = search(question, n_results=6)
    if not chunks:
        print("\nAnswer: I couldn't find anything relevant in your documents.")
        continue

    print("\nAnswer:", answer(question, chunks))

    print("\nSources:")
    for c in chunks:
        print(f"  - {c['source']} p.{c['page']} (distance {c['distance']})")