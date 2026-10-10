from src.loader import load_documents
from src.sections import split_sections

for doc in load_documents():
    secs = split_sections(doc["pages"])
    nums = [s["section"] for s in secs if s["section"] != "preamble"]
    print(f"\n{doc['source']}: {len(doc['pages'])} pages, {len(nums)} sections")
    print("first:", nums[:5], "last:", nums[-5:])
    biggest = sorted(secs, key=lambda s: len(s["text"]), reverse=True)[:3]
    print("largest sections:", [(s["section"], len(s["text"])) for s in biggest])