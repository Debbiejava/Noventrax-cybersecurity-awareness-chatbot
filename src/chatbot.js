document.getElementById("send-btn").addEventListener("click", sendMessage);

async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();

    if (message === "") return;

    addMessage(message, "user-message");
    inputField.value = "";

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

        // Show the model's reply
        addMessage(data.reply || data.error, "bot-message");

    } catch (error) {
        addMessage("Error connecting to backend.", "bot-message");
    }
}

function addMessage(text, className) {
    const chatWindow = document.getElementById("chat-window");
    const messageDiv = document.createElement("div");
    messageDiv.className = className;
    messageDiv.textContent = text;
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
