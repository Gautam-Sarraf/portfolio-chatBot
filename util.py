import os
import hashlib
import json
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


portfolio_chunks = []
portfolio_embeddings = []

CACHE_PATH = "doc/portfolio_cache.json"
INFO_PATH = "doc/gautam_sarraf_info.txt"


def get_file_hash(filepath: str) -> str:
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def initialize_portfolio():
    global portfolio_chunks, portfolio_embeddings
    if portfolio_chunks:
        return

    current_hash = get_file_hash(INFO_PATH)

    # Try to load from cache
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            if cache_data.get("hash") == current_hash:
                print("Loading portfolio data from cache...")
                portfolio_chunks = cache_data["chunks"]
                portfolio_embeddings = [
                    np.array(emb) for emb in cache_data["embeddings"]
                ]
                print(f"Loaded {len(portfolio_chunks)} chunks from cache.")
                return
        except Exception as e:
            print(f"Failed to load cache: {e}. Regenerating...")

    # Cache miss or hash mismatch: regenerate
    print("Loading portfolio data and generating embeddings...")
    portfolio_text = get_portfolio_context()
    portfolio_chunks = chunk_text(portfolio_text)
    portfolio_embeddings = [
        embed_text(chunk)
        for chunk in portfolio_chunks
    ]

    # Save to cache
    try:
        cache_data = {
            "hash": current_hash,
            "chunks": portfolio_chunks,
            "embeddings": [emb.tolist() for emb in portfolio_embeddings],
        }
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2)
        print("Embeddings cached successfully.")
    except Exception as e:
        print(f"Failed to save cache: {e}")


def retrieve_context(
    query: str,
    top_k: int = 3
):

    initialize_portfolio()
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


def generate_response_with_fallback(prompt: str) -> str:
    models_to_try = [
        "gemma-4-31b-it",
        "gemma-4-26b-a4b-it",
        "gemini-2.5-flash"
    ]

    last_error = None
    for model_name in models_to_try:
        try:
            print(f"Attempting response generation with model: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            print(f"Successfully generated response with model: {model_name}")
            return response.text
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            last_error = e

    # If all models fail, raise the last exception
    raise last_error


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

    return generate_response_with_fallback(prompt)


def generate_response_stream_with_fallback(prompt: str):
    models_to_try = [
        "gemma-4-31b-it",
        "gemma-4-26b-a4b-it",
        "gemini-2.5-flash"
    ]

    last_error = None
    for model_name in models_to_try:
        try:
            print(f"Attempting streaming response generation with model: {model_name}...")
            response = client.models.generate_content_stream(
                model=model_name,
                contents=prompt
            )
            
            stream_iter = iter(response)
            try:
                first_chunk = next(stream_iter)
            except StopIteration:
                return
            
            yield first_chunk.text
            for chunk in stream_iter:
                if chunk.text:
                    yield chunk.text
            print(f"Successfully generated streaming response with model: {model_name}")
            return
        except Exception as e:
            print(f"Model {model_name} failed for streaming: {e}")
            last_error = e

    raise last_error


def ask_portfolio_bot_stream(
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

    yield from generate_response_stream_with_fallback(prompt)

    