import { queryAll } from "../core/dom.js";

function initStoryCards() {
  const cards = queryAll("[data-story-card]");

  cards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.classList.add("scale-[1.01]", "shadow-xl");
    });

    card.addEventListener("mouseleave", () => {
      card.classList.remove("scale-[1.01]", "shadow-xl");
    });
  });
}

export function initStoryUI() {
  initStoryCards();
}
