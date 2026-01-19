document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("reset-btn").addEventListener("click", resetConversation);
document.getElementById("new-chat-btn").addEventListener("click", async () => {
    const confirmNew = confirm("Start a new chat?");
    if (!confirmNew) return;

    await fetch("http://127.0.0.1:8000/reset", { method: "POST" });
    fadeOutMessages();
});


async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();
    if (message === "") return;

    addMessage("user", message);
    inputField.value = "";

    const typingIndicator = document.getElementById("typing-indicator");
    typingIndicator.style.display = "block";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        typingIndicator.style.display = "none";

        addMessage("bot", data.reply || data.error);

    } catch (error) {
        typingIndicator.style.display = "none";
        addMessage("bot", "Error connecting to backend.");
    }
}


async function resetConversation() {
    const confirmReset = confirm("Are you sure you want to reset the conversation?");
    if (!confirmReset) return;

    try {
        await fetch("http://127.0.0.1:8000/reset", { method: "POST" });
        fadeOutMessages();
    } catch (error) {
        addMessage("bot", "Error resetting conversation.");
    }
}

    
    function fadeOutMessages() {
    const chatWindow = document.getElementById("chat-window");
    const messages = chatWindow.children;

    for (let msg of messages) {
        msg.classList.add("fade-out");
    }

    setTimeout(() => {
        chatWindow.innerHTML = "";
        addMessage("bot", "Conversation reset.");
    }, 600);
}


    function addMessage(sender, text) {
    const chatWindow = document.getElementById("chat-window");

    const messageDiv = document.createElement("div");
    messageDiv.className = sender === "user" ? "user-message" : "bot-message";
    messageDiv.textContent = text;

    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}



