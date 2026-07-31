import { getElement, queryAll } from "../core/dom.js";

function initializeMobileUX() {
  const mobileNav = getElement("mobile-nav");
  const mainContent = getElement("main-content-shell");

  if (mobileNav) {
    mobileNav.classList.add("pb-2");
  }

  if (mainContent) {
    mainContent.classList.add("pb-20", "sm:pb-6");
  }

  queryAll("[data-nav-link]").forEach((link) => {
    link.addEventListener("click", () => {
      link.classList.add("scale-[0.98]");
      window.setTimeout(() => link.classList.remove("scale-[0.98]"), 180);
    });
  });
}

export function initMobileUX() {
  initializeMobileUX();
}
