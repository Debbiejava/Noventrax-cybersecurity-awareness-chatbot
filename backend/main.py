import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware   # <-- ADD THIS

load_dotenv()

app = FastAPI()

# ✅ ADD CORS MIDDLEWARE RIGHT AFTER app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

ASSISTANT_ID = os.getenv("ASSISTANT_ID")


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = client.responses.create(
            model="gpt-5.2-chat",
            input=request.message
        )

        return {
            "reply": response.output_text
        }

    except Exception as e:
        return {
            "error": str(e)
        }
