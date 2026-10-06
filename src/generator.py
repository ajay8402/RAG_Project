from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()  # reads GEMINI_API_KEY from .env


def answer(question, chunks):
    context = "\n\n---\n\n".join(c["text"] for c in chunks)
    prompt = f"""You are a helpful assistant. Answer the question using the context below.
Explain clearly in your own words. If the context only partly answers it, share what it does say.
If the context has nothing relevant, say you don't know.

Context:
{context}

Question: {question}"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )
    return response.text