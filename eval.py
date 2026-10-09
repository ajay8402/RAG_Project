import time

from src.vectorstore import search
from src.generator import answer

# answerable=True: the PDF covers it; keywords = terms a correct answer should contain.
# answerable=False: the PDF does NOT cover it; the app should refuse.
TESTS = [
    {"q": "What is stochastic gradient descent?", "keywords": ["gradient"], "answerable": True},
    {"q": "What is the difference between supervised and unsupervised learning?", "keywords": ["label"], "answerable": True},
    {"q": "What is overfitting?", "keywords": ["overfit"], "answerable": True},
    {"q": "What is underfitting?", "keywords": ["underfit"], "answerable": True},
    {"q": "What is regularization?", "keywords": ["regulariz"], "answerable": True},
    {"q": "What is a validation set used for?", "keywords": ["validation", "hyperparameter"], "answerable": True},
    {"q": "What does Occam's razor say?", "keywords": ["simpl"], "answerable": True},
    {"q": "What is linear regression?", "keywords": ["linear"], "answerable": True},
    {"q": "Who won the 2018 World Cup?", "keywords": [], "answerable": False},
    {"q": "What is the best pizza topping?", "keywords": [], "answerable": False},
    {"q": "How do I bake sourdough bread?", "keywords": [], "answerable": False},
    {"q": "What is the capital of Australia?", "keywords": [], "answerable": False},
        # Paraphrased, answerable
    {"q": "How does a model end up memorizing training data instead of generalizing?", "keywords": ["overfit", "memoriz"], "answerable": True},
    {"q": "Why do we split off a separate part of the data when picking settings like regularization strength?", "keywords": ["validation", "hyperparameter"], "answerable": True},
    {"q": "What is the idea that no learning algorithm is best for every problem?", "keywords": ["free lunch"], "answerable": True},
    {"q": "How does a penalty on large weights help a model?", "keywords": ["weight decay", "regulariz"], "answerable": True},
    {"q": "What problem arises when the number of input dimensions grows very large?", "keywords": ["dimensionality"], "answerable": True},
    {"q": "How does PCA reduce the size of data?", "keywords": ["principal component", "variance"], "answerable": True},
    {"q": "What is k-fold cross-validation?", "keywords": ["fold", "cross-validation"], "answerable": True},
    {"q": "What does maximum likelihood estimation do?", "keywords": ["likelihood"], "answerable": True},

    # Near the topic but NOT in the PDF (should refuse)
    {"q": "How does the transformer attention mechanism work?", "keywords": [], "answerable": False},
    {"q": "How do convolutional neural networks detect edges in images?", "keywords": [], "answerable": False},
    {"q": "What is dropout and how does it prevent overfitting?", "keywords": [], "answerable": False},
    {"q": "How does early stopping work?", "keywords": [], "answerable": False},
]

REFUSAL_PHRASES = [
    "don't know", "do not know", "couldn't find", "could not find",
    "not mentioned", "no information", "not in the", "clarify",
]


def contains_any(text, words):
    text = text.lower()
    return any(w.lower() in text for w in words)


retrieval_hits = answer_hits = refusals = 0
n_answerable = sum(t["answerable"] for t in TESTS)
n_unanswerable = len(TESTS) - n_answerable
lines = []

for t in TESTS:
    chunks = search(t["q"], n_results=6)
    top = chunks[0]["distance"] if chunks else None

    if chunks:
        reply = answer(t["q"], chunks)
        time.sleep(5)  # stay under the free Gemini rate limit
    else:
        reply = "I couldn't find anything relevant in your documents."

    if t["answerable"]:
        context = " ".join(c["text"] for c in chunks)
        r_ok = contains_any(context, t["keywords"])
        a_ok = contains_any(reply, t["keywords"])
        retrieval_hits += r_ok
        answer_hits += a_ok
        line = f"{'PASS' if a_ok else 'FAIL'} | retrieval={'yes' if r_ok else 'no'} | top distance={top} | {t['q']}"
    else:
        refused = (not chunks) or contains_any(reply, REFUSAL_PHRASES)
        refusals += refused
        line = f"{'PASS' if refused else 'FAIL'} | refused={'yes' if refused else 'no'} | top distance={top} | {t['q']}"

    print(line)
    lines.append(line)

summary = [
    "",
    f"Retrieval hit rate : {retrieval_hits}/{n_answerable}",
    f"Answer accuracy    : {answer_hits}/{n_answerable}",
    f"Correct refusals   : {refusals}/{n_unanswerable}",
]
print("\n".join(summary))

with open("eval_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines + summary))