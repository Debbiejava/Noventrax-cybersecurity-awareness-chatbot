from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

AZURE_AGENT_ENDPOINT = os.getenv("AZURE_AGENT_ENDPOINT")
AZURE_AGENT_KEY = os.getenv("AZURE_AGENT_KEY")
AGENT_ID = os.getenv("AGENT_ID")

@app.post("/chat")
def chat(payload: dict):
    user_message = payload["message"]

    url = f"{AZURE_AGENT_ENDPOINT}/agents/{AGENT_ID}/chat/completions?api-version=2024-05-01-preview"

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_AGENT_KEY
    }

    body = {
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    return response.json()
