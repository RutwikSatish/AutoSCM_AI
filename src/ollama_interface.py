import requests

def ask_ollama(prompt, model="llama3.1:8b"):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=120)

        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"

        data = response.json()

        return data.get("response", "No response received.")

    except requests.exceptions.ConnectionError:
        return "❌ Ollama is not running. Run: ollama serve"

    except Exception as e:
        return f"❌ Error: {str(e)}"