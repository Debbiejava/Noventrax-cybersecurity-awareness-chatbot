import os
import time
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

AZURE_PROJECT_ENDPOINT = os.getenv("AZURE_PROJECT_ENDPOINT")
AZURE_PROJECT_API_KEY = os.getenv("AZURE_PROJECT_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

if not AZURE_PROJECT_ENDPOINT or not AZURE_PROJECT_API_KEY or not ASSISTANT_ID:
    raise ValueError("Missing one or more required environment variables.")


class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None  # optional, for future multi-turn


def _headers():
    return {
        "Content-Type": "application/json",
        "api-key": AZURE_PROJECT_API_KEY,
    }


@app.post("/chat")
def chat(request: ChatRequest):
    """
    1. Create a thread (if none provided)
    2. Add user message to thread
    3. Create a run for the assistant
    4. Poll until run completes
    5. Return latest assistant message
    """

    # 1. Create thread if not provided
    thread_id = request.thread_id
    if not thread_id:
        thread_resp = requests.post(
            f"{AZURE_PROJECT_ENDPOINT}/threads",
            headers=_headers(),
            json={}
        )
        thread_resp.raise_for_status()
        thread_id = thread_resp.json()["id"]

    # 2. Add user message
    msg_resp = requests.post(
        f"{AZURE_PROJECT_ENDPOINT}/threads/{thread_id}/messages",
        headers=_headers(),
        json={
            "role": "user",
            "content": request.message,
        },
    )
    msg_resp.raise_for_status()

    # 3. Create a run
    run_resp = requests.post(
        f"{AZURE_PROJECT_ENDPOINT}/threads/{thread_id}/runs",
        headers=_headers(),
        json={
            "assistant_id": ASSISTANT_ID,
        },
    )
    run_resp.raise_for_status()
    run_id = run_resp.json()["id"]

    # 4. Poll until run completes
    status = run_resp.json()["status"]
    while status in ("queued", "in_progress"):
        time.sleep(1)
        check_resp = requests.get(
            f"{AZURE_PROJECT_ENDPOINT}/threads/{thread_id}/runs/{run_id}",
            headers=_headers(),
        )
        check_resp.raise_for_status()
        status = check_resp.json()["status"]

    if status != "completed":
        return {
            "thread_id": thread_id,
            "status": status,
            "error": "Run did not complete successfully.",
        }

    # 5. Get messages and return latest assistant reply
    messages_resp = requests.get(
        f"{AZURE_PROJECT_ENDPOINT}/threads/{thread_id}/messages",
        headers=_headers(),
    )
    messages_resp.raise_for_status()
    messages = messages_resp.json().get("data", [])

    assistant_messages = [
        m for m in messages if m.get("role") == "assistant"
    ]
    if not assistant_messages:
        return {
            "thread_id": thread_id,
            "status": "completed",
            "reply": None,
            "note": "No assistant messages found.",
        }

    latest = assistant_messages[0]  # usually newest first
    content = latest.get("content", [])
    # content is often a list of parts; we’ll join text parts
    texts = []
    for part in content:
        if part.get("type") == "text":
            texts.append(part["text"].get("value", ""))

    reply_text = "\n".join(texts).strip()

    return {
        "thread_id": thread_id,
        "status": "completed",
        "reply": reply_text,
    }
