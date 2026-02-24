import requests
import json
import sys


def chat(prompt):
    response = requests.post(
        "http://localhost:5005/generate", json={"prompt": prompt}, timeout=120
    )
    data = response.json()
    print(f"\nYou: {prompt}")
    print(f"Bot: {data['response']}")
    if data.get("context_used"):
        print(f"(Used knowledge graph context)")
    print()


if __name__ == "__main__":
    print("Chatbot ready! Type 'quit' to exit.\n")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                break
            if user_input.strip():
                chat(user_input)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
