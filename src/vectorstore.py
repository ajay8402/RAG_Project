import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("docs")


def reset():
    global collection
    client.delete_collection("docs")
    collection = client.get_or_create_collection("docs")


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


def search(query, n_results=6):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )
    return [
        {"text": doc, "source": meta["source"], "chunk": meta["chunk"]}
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]