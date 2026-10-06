from pathlib import Path
from pypdf import PdfReader


def load_documents(folder="data"):
    docs = []
    for path in Path(folder).rglob("*"):
        suffix = path.suffix.lower()
        if suffix == ".txt":
            text = path.read_text(encoding="utf-8")
        elif suffix == ".pdf":
            reader = PdfReader(path)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            continue
        docs.append({"source": path.name, "text": text})
    return docs