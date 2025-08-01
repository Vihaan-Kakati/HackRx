import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

MODEL = "mistralai/mistral-7b-instruct"

def ask_llm(query, chunks):
    context = "\n---\n".join(chunks)
    prompt = f"""
You are an insurance policy assistant. A user has asked the following question:

Question: {query}

Refer to the following relevant sections from the insurance policy:

{context}

Based on this, provide a clear, justified decision (e.g., approved, rejected, or informational) along with the reasoning.
Return only the decision and explanation.
"""

    body = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=body)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ LLM error (OpenRouter): {str(e)}"