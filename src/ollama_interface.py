import requests

def ask_ollama(prompt, model="llama3.1:8b"):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=30)

        if response.status_code == 200:
            return response.json().get("response", "")

        return None

    except:
        return None
