document.getElementById("send-btn").addEventListener("click", sendMessage);

async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();

    if (message === "") return;

    addMessage(message, "user-message");
    inputField.value = "";

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


