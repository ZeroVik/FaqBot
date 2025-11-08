import requests
import json

OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"


def ask_ai(question: str) -> str:
    try:
        payload = {
            "model": "llama3:latest",
            "prompt": question,
            "stream": False  # easier for parsing full response
        }
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=180)

        if response.status_code == 200:
            data = response.json()
            return data.get("response", "").strip() or "No answer generated."
        else:
            return f"AI generation failed (HTTP {response.status_code}): {response.text}"
    except Exception as e:
        return f"AI generation failed: {str(e)}"
