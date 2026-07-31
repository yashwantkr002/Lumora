import { getElement, queryAll } from "../core/dom.js";

function initChatRoom() {
  const messages = getElement("chat-messages");
  const composer = getElement("chat-composer");
  const input = getElement("chat-input");

  if (!messages || !composer || !input) {
    return;
  }

  messages.scrollTop = messages.scrollHeight;

  composer.addEventListener("submit", () => {
    input.classList.add("ring-2", "ring-primary/40");
  });

  input.addEventListener("focus", () => {
    input.classList.add("ring-2", "ring-primary/40");
  });

  input.addEventListener("blur", () => {
    input.classList.remove("ring-2", "ring-primary/40");
  });
}

export function initChatUI() {
  initChatRoom();
}
