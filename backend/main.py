import os
import time
import logging
from typing import Optional, List, Dict

from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables FIRST (local dev only; Azure uses env vars/secrets)
load_dotenv()

# -----------------------------
# App + logging
# -----------------------------
app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("noventrax")


# -----------------------------
# CORS (tighten in production)
# -----------------------------
# For now keep "*" while you test; later replace with your Static Web App domain.
allow_origins = ["*"]
# Example later:
# allow_origins = [
#   "https://<your-static-app>.azurestaticapps.net",
#   "https://<your-custom-domain>"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Simple usage analytics middleware
# Logs every request: path, status, duration (ms)
# -----------------------------
@app.middleware("http")
async def request_metrics(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        return response
    finally:
        duration_ms = int((time.time() - start) * 1000)
        # note: response may not exist if an exception occurred before call_next returns
        status = getattr(locals().get("response", None), "status_code", 500)
        logger.info(
            "request path=%s method=%s status=%s duration_ms=%s",
            request.url.path,
            request.method,
            status,
            duration_ms,
        )


# -----------------------------
# Azure OpenAI client helpers
# -----------------------------
def get_client() -> Optional[OpenAI]:
    endpoint = (os.getenv("AZURE_OPENAI_ENDPOINT") or "").strip()
    api_key = (os.getenv("AZURE_OPENAI_API_KEY") or "").strip()
    if not endpoint or not api_key:
        return None
    return OpenAI(base_url=endpoint, api_key=api_key)

def get_model_name() -> Optional[str]:
    # This must be your Azure OpenAI DEPLOYMENT NAME (e.g. "gpt-5.2-chat")
    model = (os.getenv("AZURE_OPENAI_MODEL") or "").strip()
    return model or None


# -----------------------------
# System prompt + memory
# -----------------------------
SYSTEM_PROMPT = """
You are the Noventrax Cyberskills Assistant — a friendly, patient, and highly knowledgeable cybersecurity tutor.
Your mission is to help beginners and intermediate learners understand cybersecurity concepts with clarity, confidence, and practical examples.
""".strip()

conversation_history: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
MEMORY_LIMIT = 20

TRACKS = {
    "beginner": "Use simple language, explain slowly, avoid jargon, use analogies, and give small exercises.",
    "intermediate": "Use moderate technical detail, real-world examples, and scenario-based explanations.",
    "advanced": "Use deep technical detail, SOC workflows, cloud architecture, logs, and threat analysis.",
}

TOPICS = {
    "cybersecurity fundamentals": "Teach CIA triad, threats, vulnerabilities, malware, phishing, social engineering.",
    "network security": "Teach firewalls, VPNs, IDS/IPS, ports, OSI model, segmentation, zero trust.",
    "cloud security": "Teach Azure RBAC, NSGs, firewalls, key vault, defender for cloud, shared responsibility.",
    "identity and access management": "Teach MFA, SSO, OAuth, conditional access, least privilege.",
    "soc and threat detection": "Teach SIEM, SOAR, logs, MITRE ATT&CK, threat hunting, incident response.",
    "digital hygiene": "Teach passwords, safe browsing, scams, privacy, device security.",
}


# -----------------------------
# Feedback store (in-memory for now)
# NOTE: in-memory will reset when container restarts.
# Next step later: persist to App Insights, Table Storage, Cosmos DB, etc.
# -----------------------------
feedback_store: List[Dict[str, str]] = []


# -----------------------------
# Request models
# -----------------------------
class ChatRequest(BaseModel):
    message: str

class FeedbackRequest(BaseModel):
    rating: Optional[int] = None   # 1..5 optional
    comment: str
    page_url: Optional[str] = None


# -----------------------------
# Routes
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/debug-env")
def debug_env():
    return {
        "endpoint_set": bool((os.getenv("AZURE_OPENAI_ENDPOINT") or "").strip()),
        "api_key_set": bool((os.getenv("AZURE_OPENAI_API_KEY") or "").strip()),
        "model": (os.getenv("AZURE_OPENAI_MODEL") or "").strip() or None,
    }

@app.post("/feedback")
def feedback(req: FeedbackRequest):
    item = {
        "ts": str(int(time.time())),
        "rating": str(req.rating) if req.rating is not None else "",
        "comment": req.comment.strip(),
        "page_url": (req.page_url or "").strip(),
    }
    feedback_store.append(item)

    # Better than print() for Azure logs
    logger.info("[FEEDBACK] rating=%s comment=%s page=%s", item["rating"], item["comment"], item["page_url"])
    return {"status": "received"}


@app.post("/chat")
def chat(request: ChatRequest):
    global conversation_history

    msg = (request.message or "").strip()
    lower_msg = msg.lower()

    if not msg:
        return {"reply": "Please type a message."}

    # ---- Feedback via chat command ----
    # Examples:
    #   "feedback: the answer was great"
    #   "rate: 5 - very helpful"
    if lower_msg.startswith("feedback:") or lower_msg.startswith("rate:"):
        rating: Optional[int] = None
        comment = msg

        if lower_msg.startswith("rate:"):
            tail = msg.split(":", 1)[1].strip()
            parts = tail.split("-", 1)

            try:
                rating = int(parts[0].strip())
            except ValueError:
                rating = None

            comment = parts[1].strip() if len(parts) > 1 else tail

        if lower_msg.startswith("feedback:"):
            comment = msg.split(":", 1)[1].strip()

        item = {
            "ts": str(int(time.time())),
            "rating": str(rating) if rating is not None else "",
            "comment": comment,
            "page_url": "",
        }
        feedback_store.append(item)
        logger.info("[FEEDBACK(chat)] rating=%s comment=%s", item["rating"], item["comment"])
        return {"reply": "✅ Thanks! Your feedback has been recorded."}

    # ---- Track switching ----
    for track in TRACKS:
        if track in lower_msg:
            conversation_history.append({"role": "system", "content": TRACKS[track]})
            return {"reply": f"{track.title()} learning track activated."}

    # ---- Topic switching ----
    for topic in TOPICS:
        if topic in lower_msg:
            conversation_history.append({"role": "system", "content": TOPICS[topic]})
            return {"reply": f"{topic.title()} module activated. Let's begin."}

    # ---- Quizzes ----
    if "quiz" in lower_msg:
        if "network" in lower_msg:
            return {"reply": "Network Security Quiz:\n1. What is a firewall?\n2. What port does HTTPS use?\n3. Explain IDS vs IPS."}
        if "cloud" in lower_msg:
            return {"reply": "Cloud Security Quiz:\n1. What is the shared responsibility model?\n2. What is RBAC?\n3. What is an NSG?"}
        if "soc" in lower_msg:
            return {"reply": "SOC Quiz:\n1. What is SIEM?\n2. What is an IOC?\n3. What is alert triage?"}
        return {"reply": "Which topic would you like a quiz for?"}

    # ---- Normal chat flow ----
    conversation_history.append({"role": "user", "content": msg})

    # Enforce memory limit (keep the system prompt at index 0)
    if len(conversation_history) > MEMORY_LIMIT:
        conversation_history = [conversation_history[0]] + conversation_history[-(MEMORY_LIMIT - 1):]

    client = get_client()
    if client is None:
        return {"error": "Azure OpenAI is not configured. Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY."}

    model = get_model_name()
    if not model:
        return {"error": "Missing AZURE_OPENAI_MODEL (set this to your Azure OpenAI deployment name)."}

    full_input = "\n".join(f"{m['role']}: {m['content']}" for m in conversation_history)

    try:
        response = client.responses.create(
            model=model,
            input=full_input
        )
        bot_reply = response.output_text
    except Exception as e:
        logger.exception("OpenAI request failed")
        return {"error": str(e)}

    conversation_history.append({"role": "assistant", "content": bot_reply})
    return {"reply": bot_reply}


@app.post("/reset")
def reset():
    global conversation_history
    conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    return {"status": "conversation reset"}
