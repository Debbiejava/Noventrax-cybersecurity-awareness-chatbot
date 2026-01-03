# noventrax-cybersecurity-awareness-chatbot
A lightweight, browser‑based cybersecurity awareness chatbot designed to educate users on phishing, passwords, cloud security, data protection, and safe AI usage.
Built as part of a real‑world project demonstrating technical ability, governance thinking, and responsible AI design.

# Live Demo
The chatbot is live here:
http://127.0.0.1:5500/public/index.html

# Project Overview
This project is a simple, rule‑based cybersecurity awareness chatbot built using:
• 	HTML (UI structure)
• 	CSS (styling)
• 	JavaScript (chat logic + safety filters)
It is intentionally lightweight to demonstrate:
• 	Frontend development skills
• 	Safety‑first design
• 	Clear project structure
• 	Deployment capability
• 	A foundation for future AI integration (Azure OpenAI)


# Objectives
	• Promote cybersecurity awareness and safe digital behaviour
	• Demonstrate practical security thinking beyond theory
	• Explore responsible AI use in security education
	• Provide a foundation for future technical expansion

# Scope of the Chatbot
The chatbot addresses topics such as:
	• Phishing awareness
	• Password hygiene
	• Data protection principles
	• Cloud security fundamentals
	• Safe use of AI tools
	• Privacy and compliance awareness (GDPR-aligned)

# Built‑in Safety Filters
The bot blocks harmful or unethical queries such as:
- Hacking
- Bypassing security
- Illegal access

# Clean, Modern UI
- Chat window
- User and bot message styling
- Responsive layout

# Live Deployment
Hosted using GitHub Pages for easy public access.

# Project Structure
/docs
   architecture.md
   governance.md
   roadmap.md
   use-cases.md

/public
   index.html
   styles.css

/src
   chatbot.js
   safety.js

README.md

What each folder does:
- /public → UI files served to the browser
- /src → Chatbot logic and safety modules
- /docs → Architecture, governance, and roadmap documentation
- README.md → Project summary and instructions

# Architecture (Conceptual)
	[User Interface] → [Conversation Engine] → [AI Logic + Rule-Based Logic]
                     → [Governance & Safety Layer] → [Final Response]
                        +-----------------------------+
                        |        User Interface       |
                        |  (Web App / Chat Widget)    |
                        +--------------+--------------+
                                       |
                                       v
                        +-----------------------------+
                        |     Conversation Engine     |
                        |  - Intent detection         |
                        |  - Input validation         |
                        +--------------+--------------+
                                       |
                                       v
        +------------------------------+------------------------------+
        |                                                             |
        v                                                             v
+---------------------+                                   +----------------------+
|   Rule-Based Logic  |                                   |   AI Response Layer  |
| - Predefined topics |                                   | - Awareness guidance |
| - Safety rules      |                                   | - Contextual answers |
+----------+----------+                                   +----------+-----------+
           |                                                         |
           +--------------------------+------------------------------+
                                      v
                        +-----------------------------+
                        |   Governance & Safety Layer |
                        | - Ethical AI filters        |
                        | - Privacy checks            |
                        | - No personal data storage  |
                        +--------------+--------------+
                                       |
                                       v
                        +-----------------------------+
                        |       Final Response        |
                        +-----------------------------+

# Security & Governance Considerations
	• No storage of personal data
	• No automated decision-making impacting users
	• Educational purpose only
	• Transparency in AI limitations
Future versions will include:
- Input validation
- Output moderation
- Logging
- Azure OpenAI safety layers

# Roadmap
Phase 1 — UI + Rule‑Based Logic (Completed)
- Basic chatbot interface
- Predefined responses
- Safety filters
- GitHub Pages deployment
Phase 2 — Documentation (In Progress)
- README
- Architecture
- Governance
- Roadmap
Phase 3 — AI Integration (Upcoming)
- Azure OpenAI API
- Dynamic responses
- Advanced safety module
- Logging & monitoring

# Future Enhancements
	• Integration with Azure OpenAI
	• Logging and feedback mechanisms
	• Multi-language support
	• Analytics dashboard for awareness metrics

# Screenshots (to be added)
Add the following screenshots:
• 	Chatbot homepage
• 	Example conversation
• 	Folder structure in VS Code
• 	GitHub Pages deployment settings

# How to Run Locally
Clone the repository
git clone https://github.com/Debbiejava/Noventrax-cybersecurity-awareness-chatbot.git
# Open the project in VS Code
code Noventrax-cybersecurity-awareness-chatbot 
# Open index.html in your browser
Either:
- Double‑click the file, or
- Use Live Server in VS Code

# How It Works
🔹 User enters a question
The chatbot reads the input and converts it to lowercase.
🔹 Safety filter runs first
If the message contains harmful keywords (e.g., “hack”, “bypass”), the bot returns a safe response.
🔹 Awareness logic runs next
If the message matches known topics, the bot returns an educational response.
🔹 Default fallback
If the bot doesn’t understand the question, it guides the user to supported topics.

# Author
Oluwaseun Deborah Adebayo
Cybersecurity & Data Protection Practitioner
(Self-sponsored initiative)

