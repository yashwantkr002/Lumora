import { getElement, queryAll } from "../core/dom.js";

function initNotificationInteractions() {
  const cards = queryAll("[data-notification-card]");

  cards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.classList.add("shadow-lg");
    });

    card.addEventListener("mouseleave", () => {
      card.classList.remove("shadow-lg");
    });
  });
}

export function initNotificationUI() {
  initNotificationInteractions();
}
