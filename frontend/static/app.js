const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const chatWindow = document.getElementById("chat-window");

function appendMessage(text, sender = "user") {
    const div = document.createElement("div");
    div.classList.add("message", sender);
    div.textContent = text;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage(message) {
    appendMessage(message, "user");

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });

        if (!res.ok) {
            appendMessage("서버 오류가 발생했습니다.", "bot");
            return;
        }

        const data = await res.json();
        appendMessage(data.reply, "bot");
    } catch (e) {
        appendMessage("네트워크 오류가 발생했습니다.", "bot");
    }
}

form.addEventListener("submit", (e) => {
    e.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    input.value = "";
    sendMessage(message);
});
