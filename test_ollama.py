from ollama_client import ask_ollama

reply = ask_ollama("Say hello in one sentence")

print(reply)