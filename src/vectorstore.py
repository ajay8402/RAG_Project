import chromadb
from sentence_transformers import SentenceTransformer

MAX_DISTANCE = 0.65  # use a number that fits your results

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")


def _get_collection():
    return client.get_or_create_collection(
        "docs", metadata={"hnsw:space": "cosine"}
    )


collection = _get_collection()


def reset():
    global collection
    try:
        client.delete_collection("docs")
    except Exception:
        pass
    collection = _get_collection()


def add_chunks(source, chunks):
    embeddings = model.encode(chunks).tolist()
    ids = [f"{source}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source, "chunk": i} for i in range(len(chunks))]
    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search(query, n_results=6, max_distance=None):
    if max_distance is None:
        max_distance = MAX_DISTANCE
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )
    found = [
        {
            "text": doc,
            "source": meta["source"],
            "chunk": meta["chunk"],
            "distance": round(dist, 3),
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]
    return [c for c in found if c["distance"] <= max_distance]