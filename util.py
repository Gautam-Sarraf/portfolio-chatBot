import os
import numpy as np
from dotenv import load_dotenv
from google import genai
from typing import List

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def get_portfolio_context():
    with open(
        "doc/gautam_sarraf_info.txt",
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()


def chunk_text(
    text: str,
    chunk_size: int = 500
) -> List[str]:

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def embed_text(text: str):

    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )

    return np.array(
        response.embeddings[0].values
    )


def cosine_similarity(v1, v2):

    return np.dot(v1, v2) / (
        np.linalg.norm(v1)
        * np.linalg.norm(v2)
    )


print("Loading portfolio data...")

portfolio_text = get_portfolio_context()

portfolio_chunks = chunk_text(
    portfolio_text
)

portfolio_embeddings = [
    embed_text(chunk)
    for chunk in portfolio_chunks
]

print(
    f"Loaded {len(portfolio_chunks)} chunks."
)


def retrieve_context(
    query: str,
    top_k: int = 3
):

    query_embedding = embed_text(query)

    scores = []

    for idx, emb in enumerate(
        portfolio_embeddings
    ):

        score = cosine_similarity(
            query_embedding,
            emb
        )

        scores.append(
            (score, idx)
        )

    scores.sort(
        key=lambda x: x[0],
        reverse=True
    )

    contexts = []

    for score, idx in scores[:top_k]:
        contexts.append(
            portfolio_chunks[idx]
        )

    return "\n\n".join(contexts)


def ask_portfolio_bot(
    question: str,
    chat_history: list = None
):

    context = retrieve_context(
        question
    )

    history_text = ""

    if chat_history:
        for msg in chat_history:
            history_text += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

    prompt = f"""
You are Gautam Sarraf's AI Portfolio Assistant.

Rules:
- Answer as if you represent Gautam.
- Be professional and concise.
- Only use the provided context.
- If information is unavailable,
  say "I don't have information about that."

Chat History:
{history_text}

Portfolio Context:
{context}

User Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text