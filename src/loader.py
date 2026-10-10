from pathlib import Path
from pypdf import PdfReader

from src.cleaner import clean_text


def load_documents(folder="corpus"):
    docs = []
    for path in sorted(Path(folder).rglob("*")):
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            reader = PdfReader(path)
            pages = [clean_text(p.extract_text() or "") for p in reader.pages]
        elif suffix == ".txt":
            pages = [clean_text(path.read_text(encoding="utf-8"))]
        else:
            continue
        docs.append({"source": path.name, "pages": pages})
    return docs