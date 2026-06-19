import requests


RESPONSE_FORMAT = {
    "type": "object",
    "properties": {
        "bug_type": {
            "type": "string"
        },
        "explanation": {
            "type": "string"
        },
        "fixed_code": {
            "type": "string"
        },
        "confidence": {
            "type": "number"
        }
    },
    "required": [
        "bug_type",
        "explanation",
        "fixed_code",
        "confidence"
    ]
}


def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "format": RESPONSE_FORMAT,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()
        return data["response"]

    except requests.exceptions.ConnectionError:
        return None

    except requests.exceptions.Timeout:
        return None

    except requests.exceptions.RequestException:
        return None

    except KeyError:
        return None