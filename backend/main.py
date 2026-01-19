import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

conversation_history = []
MEMORY_LIMIT = 20  # optional limit


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # Add user message
        conversation_history.append({"role": "user", "content": request.message})

        # Enforce memory limit
        if len(conversation_history) > MEMORY_LIMIT:
            conversation_history.pop(0)

        # Build full conversation text
        full_input = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in conversation_history]
        )

        # Send to Azure
        response = client.responses.create(
            model="gpt-5.2-chat",
            input=full_input
        )

        bot_reply = response.output_text

        # Add bot reply
        conversation_history.append({"role": "assistant", "content": bot_reply})

        return {"reply": bot_reply}

    except Exception as e:
        return {"error": str(e)}


@app.post("/reset")
def reset():
    conversation_history.clear()
    return {"status": "conversation reset"}
