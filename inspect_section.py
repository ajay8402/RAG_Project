import sys

from src.vectorstore import collection

source, section = sys.argv[1], sys.argv[2]
res = collection.get(where={"$and": [{"source": source}, {"section": section}]})
for doc, meta in zip(res["documents"], res["metadatas"]):
    print(f"--- page {meta['page']} chunk {meta['chunk']} ({len(doc)} chars)")
    print(doc, "\n")