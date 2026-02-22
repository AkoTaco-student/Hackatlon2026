import { AvatarStream } from "./avatarStream.js";

const chatBox = document.getElementById("chatBox");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const loading = document.getElementById("loading");

const avatarVideo = document.getElementById("avatarVideo");
const avatarStatus = document.getElementById("avatarStatus");
const avatarStartBtn = document.getElementById("avatarStartBtn");
const avatarStopBtn = document.getElementById("avatarStopBtn");

const API_STREAM_URL = "/api/chat";

const avatarStream = new AvatarStream(avatarVideo, avatarStatus);

avatarStartBtn.addEventListener("click", async () => {
  avatarStartBtn.disabled = true;
  try {
    await avatarStream.init();
    avatarStopBtn.disabled = false;
  } catch (err) {
    avatarStatus.textContent = err.message;
    avatarStartBtn.disabled = false;
  }
});

avatarStopBtn.addEventListener("click", async () => {
  avatarStopBtn.disabled = true;
  await avatarStream.stop();
  avatarStatus.textContent = "Avatar stopped";
  avatarStartBtn.disabled = false;
});

// Send message on button click
sendBtn.addEventListener("click", sendMessage);

// Send message on Enter key
messageInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

async function sendMessage() {
  const message = messageInput.value.trim();

  if (!message) return;

  addMessageToChat(message, "user");
  messageInput.value = "";
  sendBtn.disabled = true;
  loading.style.display = "flex";

  const aiMessage = addMessageToChat("", "ai");
  let fullText = "";

  try {
    const response = await fetch(API_STREAM_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok || !response.body) {
      throw new Error("Network response was not ok");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      let parts = buffer.split("\n\n");
      buffer = parts.pop() || "";

      for (const part of parts) {
        const line = part.split("\n").find((l) => l.startsWith("data: "));
        if (!line) continue;
        const payload = JSON.parse(line.replace("data: ", ""));
        if (payload.type === "chunk") {
          fullText += payload.text;
          aiMessage.textContent = fullText;
          chatBox.scrollTop = chatBox.scrollHeight;
          avatarStream.speak(payload.text);
        } else if (payload.type === "error") {
          throw new Error(payload.error);
        }
      }
    }
  } catch (error) {
    console.error("Error:", error);
    aiMessage.textContent =
      "Beklager, jeg kunne ikke kontakte serveren. Er Ollama kjørende?";
  } finally {
    sendBtn.disabled = false;
    loading.style.display = "none";
    messageInput.focus();
  }
}

function addMessageToChat(message, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}-message`;

  const p = document.createElement("p");
  p.textContent = message;

  messageDiv.appendChild(p);
  chatBox.appendChild(messageDiv);

  chatBox.scrollTop = chatBox.scrollHeight;
  return p;
}
