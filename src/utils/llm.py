import requests
import os
from typing import List, Dict


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


class LLMError(Exception):
    pass


def chat_completion(system_prompt: str, messages: List[Dict[str, str]], model_name: str = None) -> str:
    """
    Local Ollama LLM wrapper.

    Produces more realistic, detailed outputs by using:
    - Higher max_tokens (4096)
    - Temperature 0.3
    """

    # Build combined prompt with roles
    prompt = f"System:\n{system_prompt.strip()}\n\n"

    for m in messages:
        role = m.get("role", "user").capitalize()
        content = m.get("content", "").strip()
        prompt += f"{role}:\n{content}\n\n"

    model = model_name or MODEL_NAME
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 4096,     # MORE REALISTIC LONG OUTPUT
        "temperature": 0.3,     # SLIGHT VARIATION, MORE HUMAN
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=180)
    except requests.RequestException as e:
        raise LLMError(f"Request to Ollama failed: {e}")

    if r.status_code != 200:
        raise LLMError(f"Ollama returned {r.status_code}: {r.text}")

    data = r.json()

    # Primary keys Ollama uses
    if "response" in data:
        return data["response"]

    if "text" in data:
        return data["text"]

    # Fallback for future Ollama formats
    if "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0].get("message", {}).get("content", "")

    # Final fallback
    return str(data)
