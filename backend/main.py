import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# TODO: once deployed, replace "*" with your actual frontend URL(s)
allow_origins = ["*"]
# allow_origins = [
#     "https://<your-static-app>.azurestaticapps.net",
#     "https://<your-custom-domain>",
# ]

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# System prompt
SYSTEM_PROMPT = """
You are the Noventrax Cyberskills Assistant — a friendly, patient, and highly knowledgeable cybersecurity tutor.
Your mission is to help beginners and intermediate learners understand cybersecurity concepts with clarity, confidence, and practical examples.
"""

# Conversation memory (in-memory; resets if container restarts)
conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# Learning tracks
TRACKS = {
    "beginner": "Use simple language, explain slowly, avoid jargon, use analogies, and give small exercises.",
    "intermediate": "Use moderate technical detail, real-world examples, and scenario-based explanations.",
    "advanced": "Use deep technical detail, SOC workflows, cloud architecture, logs, and threat analysis.",
}

# Topic modules
TOPICS = {
    "cybersecurity fundamentals": "Teach CIA triad, threats, vulnerabilities, malware, phishing, social engineering.",
    "network security": "Teach firewalls, VPNs, IDS/IPS, ports, OSI model, segmentation, zero trust.",
    "cloud security": "Teach Azure RBAC, NSGs, firewalls, key vault, defender for cloud, shared responsibility.",
    "identity and access management": "Teach MFA, SSO, OAuth, conditional access, least privilege.",
    "soc and threat detection": "Teach SIEM, SOAR, logs, MITRE ATT&CK, threat hunting, incident response.",
    "digital hygiene": "Teach passwords, safe browsing, scams, privacy, device security.",
}

MEMORY_LIMIT = 20


class ChatRequest(BaseModel):
    message: str


def get_client() -> OpenAI | None:
    """
    Create Azure OpenAI client lazily so the app can boot even if env vars are missing.
    This keeps /health working.
    """
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if not endpoint or not api_key:
        return None
    return OpenAI(base_url=endpoint, api_key=api_key)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    global conversation_history

    try:
        lower_msg = request.message.lower().strip()

        # Track switching
        for track in TRACKS:
            if track in lower_msg:
                conversation_history.append({"role": "system", "content": TRACKS[track]})
                return {"reply": f"{track.title()} learning track activated."}

        # Topic switching
        for topic in TOPICS:
            if topic in lower_msg:
                conversation_history.append({"role": "system", "content": TOPICS[topic]})
                return {"reply": f"{topic.title()} module activated. Let's begin."}

        # Quizzes
        if "quiz" in lower_msg:
            if "network" in lower_msg:
                return {"reply": "Network Security Quiz:\n1. What is a firewall?\n2. What port does HTTPS use?\n3. Explain IDS vs IPS."}
            if "cloud" in lower_msg:
                return {"reply": "Cloud Security Quiz:\n1. What is the shared responsibility model?\n2. What is RBAC?\n3. What is an NSG?"}
            if "soc" in lower_msg:
                return {"reply": "SOC Quiz:\n1. What is SIEM?\n2. What is an IOC?\n3. What is alert triage?"}
            return {"reply": "Which topic would you like a quiz for? (network / cloud / soc)"}

        # Add user message
        conversation_history.append({"role": "user", "content": request.message})

        # Enforce memory limit (keep the system prompt at index 0)
        if len(conversation_history) > MEMORY_LIMIT:
            conversation_history = [conversation_history[0]] + conversation_history[-(MEMORY_LIMIT - 1):]

        # Build conversation text
        full_input = "\n".join(
            f"{msg['role']}: {msg['content']}" for msg in conversation_history
        )

        # Lazily get client
        client = get_client()
        if client is None:
            return {"error": "Azure OpenAI is not configured. Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY."}

        # Get model/deployment name
        model = os.getenv("AZURE_OPENAI_MODEL")
        if not model:
            return {"error": "Missing AZURE_OPENAI_MODEL (set this to your Azure OpenAI deployment name)."}

        # Azure OpenAI call
        response = client.responses.create(
            model=model,      # <-- THIS is what “use model=model in the request” means
            input=full_input
        )

        bot_reply = response.output_text or "I couldn't generate a response. Please try again."

        # Add assistant reply
        conversation_history.append({"role": "assistant", "content": bot_reply})

        return {"reply": bot_reply}

    except Exception as e:
        return {"error": str(e)}


@app.post("/reset")
def reset():
    global conversation_history
    conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    return {"status": "conversation reset"}
