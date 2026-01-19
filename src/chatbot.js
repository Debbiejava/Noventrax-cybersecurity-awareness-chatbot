document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("reset-btn").addEventListener("click", resetConversation);
document.getElementById("new-chat-btn").addEventListener("click", async () => {
    const confirmNew = confirm("Start a new chat?");
    const API_URL = "http://127.0.0.1:8000/chat";

    if (!confirmNew) return;

    await fetch("http://127.0.0.1:8000/reset", { method: "POST" });

    fadeOutMessages();
});

async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();

    if (message === "") return;

    addMessage(message, "user-message");
    inputField.value = "";

async function resetConversation() {
    const confirmReset = confirm("Are you sure you want to reset the conversation?");
    if (!confirmReset) return;

    try {
        await fetch("http://127.0.0.1:8000/reset", { method: "POST" });

        fadeOutMessages(); // trigger fade-out animation

    } catch (error) {
        addMessage("Error resetting conversation.", "bot-message");
    }
}
    
    // Show typing indicator
    const typingIndicator = document.getElementById("typing-indicator");
    typingIndicator.style.display = "block";


    // Call your backend instead of using getBotResponse()
    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        // Hide typing indicator
        typingIndicator.style.display = "none";

        addMessage(data.reply || data.error, "bot-message");

    } catch (error) {
        typingIndicator.style.display = "none";
        addMessage("Error connecting to backend.", "bot-message");
    }
}

async function resetConversation() {
    try {
        const response = await fetch("http://127.0.0.1:8000/reset", {
            method: "POST"
        });

        const data = await response.json();

        // Clear the chat window visually
        const chatWindow = document.getElementById("chat-window");
        chatWindow.innerHTML = "";

        // Optional: show confirmation message
        addMessage("Conversation reset.", "bot-message");

    } catch (error) {
        addMessage("Error resetting conversation.", "bot-message");
    }
    
    function fadeOutMessages() {
    const chatWindow = document.getElementById("chat-window");
    const messages = chatWindow.children;

    for (let msg of messages) {
        msg.classList.add("fade-out");
    }

    setTimeout(() => {
        chatWindow.innerHTML = "";
        addMessage("Conversation reset.", "bot-message");
    }, 600);
}
}


