from pathlib import Path

import streamlit as st

from src.loader import load_documents
from src.chunker import chunk_text
from src.vectorstore import add_chunks, search
from src.generator import answer

st.set_page_config(page_title="RAG Chat", page_icon="📄")
st.title("📄 Chat with your documents")

# ---------- Sidebar: add a new document ----------
with st.sidebar:
    st.header("Add a document")
    uploaded = st.file_uploader("PDF or TXT", type=["pdf", "txt"])
    if uploaded and st.button("Add to knowledge base"):
        Path("data").mkdir(exist_ok=True)
        (Path("data") / uploaded.name).write_bytes(uploaded.getvalue())
        with st.spinner("Reading and embedding..."):
            for doc in load_documents():
                if doc["source"] == uploaded.name:
                    chunks = chunk_text(doc["text"])
                    add_chunks(doc["source"], chunks)
                    st.success(f"Added {len(chunks)} chunks from {uploaded.name}")

# ---------- Chat history ----------
if "messages" not in st.session_state:
    st.session_state.messages = []


def show_sources(sources):
    with st.expander("Sources"):
        for c in sources:
            st.markdown(f"**{c['source']}** (chunk {c['chunk']}, distance {c['distance']})")
            st.caption(c["text"][:300] + "...")


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            show_sources(msg["sources"])

# ---------- New question ----------
if question := st.chat_input("Ask a question about your documents"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chunks = search(question, n_results=6)
            if chunks:
                reply = answer(question, chunks)
            else:
                reply = "I couldn't find anything relevant in your documents."
        st.markdown(reply)
        if chunks:
            show_sources(chunks)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply, "sources": chunks}
    )