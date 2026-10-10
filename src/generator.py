from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()  # reads GEMINI_API_KEY from .env

MODEL = "gemini-3.5-flash-lite"


def _format_history(history):
    lines = []
    for m in history:
        who = "User" if m["role"] == "user" else "Assistant"
        lines.append(f"{who}: {m['content']}")
    return "\n".join(lines)


def rewrite_question(question, history):
    """Turn a follow-up like 'explain that simpler' into a standalone question."""
    if not history:
        return question

    prompt = f"""Given the conversation and the follow-up question, rewrite the follow-up
as one standalone question that makes sense without the conversation.
If it is already standalone, return it unchanged. Return only the question.

Conversation:
{_format_history(history)}

Follow-up question: {question}"""

    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text.strip()


def answer(question, chunks, history=None):
    context = "\n\n---\n\n".join(
        f"[{c['source']}, page {c['page']}]\n{c['text']}" for c in chunks
    )
    convo = _format_history(history) if history else "(no earlier messages)"

    prompt = f"""You are an assistant that explains Indian public legal documents in plain language.
Use only the context below. Do not use your own general knowledge.
If the context has nothing relevant, say you don't know and suggest checking the official source or a lawyer.
If the context only partly answers the question, share what it does say.
When you state a rule, cite its page like (page 12).
Reply in the same language as the question.
Describe what the document says. Do not give legal advice or predict the outcome of a case.
Use the earlier conversation only to understand what the question refers to.
If the question is vague and the earlier conversation does not explain what it refers to, ask the user to clarify instead of guessing.

Earlier conversation:
{convo}

Context:
{context}

Question: {question}"""

    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text