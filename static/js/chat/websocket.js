import { getElement } from "../core/dom.js";

function initWebsocketChat() {
  const chatMessages = getElement("chat-messages");
  const composer = getElement("chat-composer");
  const input = getElement("chat-input");

  if (!chatMessages || !composer || !input) {
    return;
  }

  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const wsUrl = `${protocol}://${window.location.host}/ws/chat/`;

  try {
    const socket = new WebSocket(wsUrl);

    socket.addEventListener("open", () => {
      const status = getElement("chat-status");
      if (status) {
        status.textContent = "Connected live";
      }
    });

    socket.addEventListener("message", (event) => {
      const status = getElement("chat-status");
      if (status) {
        status.textContent = "New message synced";
      }
      console.info("WebSocket message received", event.data);
    });

    composer.addEventListener("submit", (event) => {
      const message = input.value.trim();
      if (!message) {
        event.preventDefault();
        return;
      }

      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ message }));
      }
    });
  } catch (error) {
    console.warn("WebSocket unavailable", error);
  }
}

export function initWebSocketChat() {
  initWebsocketChat();
}
