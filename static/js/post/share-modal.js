import { getElement, queryAll } from "../core/dom.js";

function initShareModal() {
  const triggers = queryAll("[data-share-trigger]");
  const modal = getElement("share-modal");
  const closeButton = getElement("share-modal-close");
  const backdrop = getElement("share-modal-backdrop");
  const fields = queryAll("[data-share-field]");

  if (!modal) {
    return;
  }

  const open = () => {
    modal.classList.remove("hidden");
    modal.classList.add("flex");
    document.body.classList.add("overflow-hidden");
    const firstField = fields[0];
    firstField?.focus();
  };

  const close = () => {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    document.body.classList.remove("overflow-hidden");
  };

  triggers.forEach((trigger) => {
    trigger.addEventListener("click", open);
  });

  closeButton?.addEventListener("click", close);
  backdrop?.addEventListener("click", close);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !modal.classList.contains("hidden")) {
      close();
    }
  });
}

export function initShareComposer() {
  initShareModal();
}
