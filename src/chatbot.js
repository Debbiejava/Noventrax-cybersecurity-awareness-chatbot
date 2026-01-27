/* DOM ELEMENT REFERENCES */
const API_BASE = window.API_BASE_URL || "";
const sendBtn = document.getElementById("send-btn");
const resetBtn = document.getElementById("reset-btn");
const newChatBtn = document.getElementById("new-chat-btn");
const inputField = document.getElementById("user-input");
const chatWindow = document.getElementById("chat-window");
const typingIndicator = document.getElementById("typing-indicator");
const themeToggle = document.getElementById("theme-toggle");
const dashboard = document.getElementById("dashboard");
let chatMessages = [];


/* EVENT LISTENERS */

// Send button
sendBtn.addEventListener("click", sendMessage);

// Reset button
resetBtn.addEventListener("click", resetConversation);

// New chat button
newChatBtn.addEventListener("click", async () => {
    const confirmNew = confirm("Start a new chat?");
    if (!confirmNew) return;

    await fetch(`${API_BASE}/reset`, { method: "POST" });
    fadeOutMessages();
});

// Enter-to-send
inputField.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendBtn.click();
    }
});

// Topic buttons
document.querySelectorAll(".topic-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const topic = btn.dataset.topic;
        sendMessageDirect(`start ${topic}`);
    });
});

// Theme toggle
themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");

    const isDark = document.body.classList.contains("dark-mode");
    localStorage.setItem("theme", isDark ? "dark" : "light");

    themeToggle.textContent = isDark ? "☀️" : "🌙";
});

// Load saved theme
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
    themeToggle.textContent = "☀️";
}


/* CHAT FUNCTIONS */

// Send message normally
async function sendMessage() {
    const message = inputField.value.trim();
    if (message === "") return;

    hideDashboard();
    addMessage("user", message);
    inputField.value = "";

    typingIndicator.style.display = "block";

    try {
        const response = await fetch(`${API_BASE}/chat`, {
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

// Send message directly (used for topic buttons)
async function sendMessageDirect(message) {
    hideDashboard();
    addMessage("user", message);

    const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    addMessage("bot", data.reply);
}

// Add message to chat window
function addMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.className = sender === "user" ? "user-message" : "bot-message";
    messageDiv.textContent = text;

    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    chatMessages.push({ role: sender, content: text });
}


/* RESET & UI EFFECTS */

async function resetConversation() {
    const confirmReset = confirm("Are you sure you want to reset the conversation?");
    if (!confirmReset) return;

    try {
        await fetch(`${API_BASE}/reset`, { method: "POST" });
        fadeOutMessages();
    } catch (error) {
        addMessage("bot", "Error resetting conversation.");
    }
}

function fadeOutMessages() {
    const messages = chatWindow.children;

    for (let msg of messages) {
        msg.classList.add("fade-out");
    }

    setTimeout(() => {
        chatWindow.innerHTML = "";
        chatMessages = [];
        addMessage("bot", "Conversation reset.");
    }, 600);
}

function hideDashboard() {
    dashboard.style.display = "none";
}


/* CHAT HISTORY (LOCAL STORAGE) */

function saveChatSession() {
    const history = JSON.parse(localStorage.getItem("chatHistory") || "[]");

    history.push({
        id: Date.now(),
        title: "Chat " + new Date().toLocaleTimeString(),
        messages: chatMessages
    });

    localStorage.setItem("chatHistory", JSON.stringify(history));
}

function loadHistory() {
    const history = JSON.parse(localStorage.getItem("chatHistory") || "[]");
    const list = document.getElementById("history-list");

    list.innerHTML = "";

    history.forEach(session => {
        const li = document.createElement("li");
        li.textContent = session.title;
        li.dataset.id = session.id;

        li.addEventListener("click", () => loadChatSession(session.id));

        list.appendChild(li);
    });
}

function loadChatSession(id) {
    const history = JSON.parse(localStorage.getItem("chatHistory") || "[]");
    const session = history.find(s => s.id == id);

    if (!session) return;

    chatMessages = session.messages;
    renderChatMessages();
}

function renderChatMessages() {
    chatWindow.innerHTML = "";

    chatMessages.forEach(msg => {
        addMessage(msg.role, msg.content);
    });

    chatWindow.scrollTop = chatWindow.scrollHeight;
}


/* INITIALIZATION */
loadHistory();
