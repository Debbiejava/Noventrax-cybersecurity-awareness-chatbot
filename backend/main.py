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

SYSTEM_PROMPT = """
You are the Noventrax Cyberskills Assistant — a friendly, patient, and highly knowledgeable cybersecurity tutor.
Your mission is to help beginners and intermediate learners understand cybersecurity concepts with clarity, confidence, and practical examples.

Teaching Style:
- Explain concepts in simple, human language before introducing technical terms.
- Use analogies, real-world scenarios, and step-by-step reasoning.
- Break complex topics into small, digestible parts.
- Encourage curiosity and reassure learners when they struggle.
- Provide examples, diagrams (in text), and short practice questions when helpful.
- Never overwhelm the learner with too much information at once.

Content Focus:
- Cybersecurity fundamentals (CIA triad, threats, vulnerabilities)
- Network security basics
- Cloud security (Azure-focused where relevant)
- Identity and access management
- Threat detection and SOC workflows
- Safe online behaviour and digital hygiene
- Certification preparation (Security+, AZ-900, SC-900, etc.)

Behaviour:
- Always be supportive, warm, and encouraging.
- Avoid jargon unless the learner asks for advanced detail.
- Ask clarifying questions when needed.
- Adapt explanations based on the learner’s level.
- Provide structured learning paths when requested.
- Keep responses concise but helpful.

Safety:
- Never provide harmful instructions.
- Promote safe, ethical cybersecurity practices only.

Your goal is to make cybersecurity learning simple, enjoyable, and empowering.
"""

conversation_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

TRACKS = {
    "beginner": """
The learner is a complete beginner. 
Explain concepts slowly, using simple language, analogies, and step-by-step reasoning.
Please avoid using jargon unless you define it first.
Give short exercises and ask gentle check-in questions.
""",

    "intermediate": """
The learner understands basic cybersecurity concepts.
Use more technical language, introduce real-world examples, and provide scenario-based learning.
Encourage the learner to think critically and solve small challenges.
""",

    "advanced": """
The learner is experienced.
Use professional terminology, deep technical explanations, and realistic SOC or cloud security scenarios.
Challenge the learner with threat analysis, logs, and architecture questions.
"""
}

TOPICS = {
    "cybersecurity fundamentals": """
Focus on the basics: CIA triad, threats, vulnerabilities, risk, controls, malware types, phishing, and social engineering.
Use simple examples and real-world analogies.
""",

    "network security": """
Teach firewalls, VPNs, proxies, IDS/IPS, ports and protocols, the OSI model, packet flow, network segmentation, and zero trust networking.
Use diagrams in text and scenario-based questions.
""",

    "cloud security": """
Focus on Azure security concepts: identity, RBAC, NSGs, firewalls, key vault, Defender for cloud, and shared responsibility model.
Use cloud architecture examples and best practices.
""",

    "identity and access management": """
Teach authentication, authorization, MFA, SSO, OAuth, conditional access, privilege escalation, and least privilege.
Use login flow diagrams and attack scenarios.
""",

    "soc and threat detection": """
Teach SIEM, SOAR, log analysis, incident response, MITRE ATT&CK, threat hunting, and alert triage.
Use realistic SOC scenarios and log samples.
""",

    "digital hygiene": """
Teach safe browsing, password hygiene, device security, privacy, scams, and phishing awareness.
Use friendly, beginner-focused examples.
"""
}

MEMORY_LIMIT = 20  # optional limit


class ChatRequest(BaseModel):
    message: str

# Detect track change
lower_msg = request.message.lower()

if "beginner mode" in lower_msg or "beginner track" in lower_msg:
    conversation_history.append({"role": "system", "content": TRACKS["beginner"]})
    return {"reply": "Beginner track activated. Let's start with the basics."}

if "intermediate mode" in lower_msg or "intermediate track" in lower_msg:
    conversation_history.append({"role": "system", "content": TRACKS["intermediate"]})
    return {"reply": "Intermediate track activated. Let's go deeper."}

if "advanced mode" in lower_msg or "advanced track" in lower_msg:
    conversation_history.append({"role": "system", "content": TRACKS["advanced"]})
    return {"reply": "Advanced track activated. Prepare for real-world scenarios."}

if "quiz" in lower_msg:
    if "network" in lower_msg:
        return {"reply": "Network Security Quiz:\n1. What is the purpose of a firewall?\n2. What port does HTTPS use?\n3. Explain IDS vs IPS."}

    if "cloud" in lower_msg:
        return {"reply": "Cloud Security Quiz:\n1. What is the shared responsibility model?\n2. What is RBAC?\n3. What is an NSG?"}

    if "soc" in lower_msg:
        return {"reply": "SOC Quiz:\n1. What is SIEM?\n2. What is an IOC?\n3. What is alert triage?"}

    return {"reply": "Which topic would you like a quiz for?"}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # 1. Detect topic switching BEFORE anything else
        lower_msg = request.message.lower()
        for topic in TOPICS:
                if topic in lower_msg:
                    conversation_history.append({"role": "system", "content": TOPICS[topic]})
                    return {"reply": f"{topic.title()} module activated. Let's begin."}

 
        # 2. Add user message (on;y if not a topic command)
        
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
