import streamlit as st

from src.vectorstore import search
from src.generator import answer, rewrite_question

st.set_page_config(page_title="Citizen Rights Assistant", page_icon="⚖️")
st.title("⚖️ Citizen Rights Assistant")
st.caption(
    "Answers from Indian public legal documents, with page citations. "
    "General information only, not legal advice."
)

with st.sidebar:
    st.header("About")
    st.write("Indexed: Consumer Protection Act, 2019 (source: India Code).")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []


def show_sources(sources):
    with st.expander("Sources"):
        for c in sources:
            st.markdown(
                f"**{c['source']}**, PDF page {c.get('page', '?')} "
                f"(distance {c['distance']})"
            )
            st.caption(c["text"][:300] + "...")


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            show_sources(msg["sources"])

if question := st.chat_input("Ask about your rights, e.g. how to file a consumer complaint"):
    history = st.session_state.messages[-6:]

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the Act..."):
            search_query = rewrite_question(question, history)
            chunks = search(search_query, n_results=6)
            if chunks:
                reply = answer(question, chunks, history)
            else:
                reply = "I couldn't find anything relevant in the indexed documents."
        st.markdown(reply)
        if chunks:
            show_sources(chunks)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply, "sources": chunks}
    )
    