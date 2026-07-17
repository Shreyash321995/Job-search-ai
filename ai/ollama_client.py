import os
import time
import requests

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434/api/generate"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "phi3"
)


def generate_response(prompt):

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    start = time.time()

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        print("=" * 60)
        print("Model :", OLLAMA_MODEL)
        print("Time  :", round(time.time() - start, 2), "sec")
        print("=" * 60)

        return response.json()["response"]

    except Exception as e:
        return f"Interview Analysis Error: {e}"
