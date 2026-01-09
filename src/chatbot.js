document.getElementById("send-btn").addEventListener("click", sendMessage);

function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();

    if (message === "") return;

    addMessage(message, "user-message");
    inputField.value = "";

    const response = getBotResponse(message);
    addMessage(response, "bot-message");
}

function addMessage(text, className) {
    const chatWindow = document.getElementById("chat-window");
    const messageDiv = document.createElement("div");
    messageDiv.className = className;
    messageDiv.textContent = text;
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function getBotResponse(message) {
    const lower = message.toLowerCase();

    // Safety filter
    if (lower.includes("hack") || lower.includes("bypass")) {
        return "I can’t assist with hacking or bypassing security, but I can help you learn how to protect yourself from cyber threats.";
    }

    // Awareness topics
    if (lower.includes("phishing")) {
        return "Phishing emails often use urgency, suspicious links, or unexpected requests. Always verify the sender and avoid clicking unknown links.";
    }

    if (lower.includes("password")) {
        return "Use long, unique passwords and enable multi-factor authentication. A password manager can help you stay secure.";
    }

    if (lower.includes("cloud")) {
        return "Cloud security follows a shared responsibility model. Use strong access controls and avoid sharing public links.";
    }

    if (lower.includes("ai") || lower.includes("chatgpt")) {
        return "Avoid sharing personal or sensitive data with AI tools. Use them responsibly and verify important information.";
    }

    if (lower.includes("data") || lower.includes("privacy")) {
        return "Protect your personal data by limiting what you share online and reviewing privacy settings regularly.";
    }

    return "I'm here to help with cybersecurity awareness and skill acquisition. Try asking about phishing, passwords, cloud security, data protection, or AI safety.";
}
