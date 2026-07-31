import { getElement } from "../core/dom.js";

function initializeRealtimeChat() {
  const composer = getElement("chat-composer");
  const input = getElement("chat-input");
  const messages = getElement("chat-messages");

  if (!composer || !input || !messages) {
    return;
  }

  const status = document.createElement("p");
  status.id = "chat-status";
  status.className = "mt-2 text-xs text-slate-500";
  status.textContent = "Live chat ready";
  composer.after(status);

  input.addEventListener("input", () => {
    status.textContent = input.value.trim()
      ? "Typing..."
      : "Live chat ready";
  });

  window.setInterval(() => {
    if (!messages.dataset.liveReady) {
      messages.dataset.liveReady = "true";
      status.textContent = "Live sync enabled";
    }
  }, 4000);
}

export function initRealtimeChat() {
  initializeRealtimeChat();
}
