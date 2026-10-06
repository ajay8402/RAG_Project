from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()  # reads GEMINI_API_KEY from .env


def answer(question, chunks):
    context = "\n\n---\n\n".join(chunks)
    prompt = f"""Answer the question using only the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question: {question}"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )
    return response.text