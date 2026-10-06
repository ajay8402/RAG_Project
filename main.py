from src.vectorstore import search
from src.generator import answer

print("Ask questions about your document. Type 'exit' to quit.")

while True:
    question = input("\nYou: ").strip()
    if question.lower() in ("exit", "quit"):
        break
    if not question:
        continue

    chunks = search(question, n_results=4)
    print("\nAnswer:", answer(question, chunks))