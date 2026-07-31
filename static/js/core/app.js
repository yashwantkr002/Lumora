import { getElement, queryAll } from "./dom.js";
import { initSocialInteractions } from "../post/interactions.js";
import { initInfiniteFeed } from "../post/infinite-feed.js";
import { initShareComposer } from "../post/share-modal.js";
import { initNotificationUI } from "../notifications/notifications.js";
import { initStoryUI } from "../stories/stories.js";
import { initStoryViewerUI } from "../stories/viewer.js";
import { initChatUI } from "../chat/chat.js";
import { initRealtimeChat } from "../chat/realtime.js";
import { initWebSocketChat } from "../chat/websocket.js";
import { initMobileUX } from "../mobile/ux.js";

const THEME_STORAGE_KEY = "theme";
const DARK_CLASS = "dark";

function setTheme(theme) {
  const isDark = theme === "dark";
  const root = document.documentElement;

  root.classList.toggle(DARK_CLASS, isDark);
  root.setAttribute("data-theme", isDark ? "dark" : "light");
  root.style.colorScheme = isDark ? "dark" : "light";

  const toggles = queryAll("[data-theme-toggle]");

  toggles.forEach((toggle) => {
    const icon = toggle.querySelector("i");

    if (!icon) return;

    icon.className = isDark ? "fa-solid fa-sun" : "fa-solid fa-moon";
    toggle.setAttribute("aria-pressed", String(isDark));
  });
}

function initTheme() {
  const storedTheme = localStorage.getItem(THEME_STORAGE_KEY);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const initialTheme = storedTheme ?? (prefersDark ? "dark" : "light");

  setTheme(initialTheme);

  queryAll("[data-theme-toggle]").forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const isDark = document.documentElement.classList.contains(DARK_CLASS);
      const nextTheme = isDark ? "light" : "dark";

      localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
      setTheme(nextTheme);
    });
  });
}

function initBackToTop() {
  const button = getElement("backToTop");

  if (!button) return;

  const toggleVisibility = () => {
    const shouldShow = window.scrollY > 320;
    button.classList.toggle("hidden", !shouldShow);
  };

  toggleVisibility();

  window.addEventListener("scroll", () => {
    requestAnimationFrame(toggleVisibility);
  }, { passive: true });

  button.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

function initLoader() {
  const loader = getElement("page-loader");

  if (!loader) return;

  window.addEventListener(
    "load",
    () => {
      requestAnimationFrame(() => {
        loader.classList.add("opacity-0", "pointer-events-none");
        window.setTimeout(() => loader.remove(), 320);
      });
    },
    { once: true },
  );
}

function initNavigation() {
  const links = queryAll("[data-nav-link]");

  if (!links.length) return;

  const currentPath = window.location.pathname;

  links.forEach((link) => {
    const href = link.getAttribute("href") ?? "";

    if (!href || href === "#") return;

    const normalizedHref = href.replace(window.location.origin, "");
    const isActive = normalizedHref === "/"
      ? currentPath === "/"
      : currentPath.startsWith(normalizedHref);

    link.classList.toggle("text-primary", isActive);
    link.classList.toggle("dark:text-primary", isActive);
    link.classList.toggle("text-slate-600", !isActive);
    link.classList.toggle("dark:text-slate-300", !isActive);
  });
}

function initMessages() {
  const container = getElement("messages-container");

  if (!container) return;

  const items = container.querySelectorAll(":scope > div");

  items.forEach((item) => {
    const dismissButton = item.querySelector("[data-dismiss-message]");

    if (dismissButton) {
      dismissButton.addEventListener("click", () => item.remove());
    }
  });

  window.setTimeout(() => {
    items.forEach((item) => item.remove());
  }, 5000);
}

function initRevealAnimations() {
  if (!("IntersectionObserver" in window)) {
    return;
  }

  const elements = queryAll("[data-reveal]");

  if (!elements.length) return;

  elements.forEach((element) => {
    element.classList.add("opacity-0", "translate-y-4", "transition-all", "duration-500");
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;

      entry.target.classList.remove("opacity-0", "translate-y-4");
      entry.target.classList.add("opacity-100", "translate-y-0");
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.15 });

  elements.forEach((element) => observer.observe(element));
}

function init() {
  initTheme();
  initLoader();
  initBackToTop();
  initNavigation();
  initMessages();
  initRevealAnimations();
  initSocialInteractions();
  initInfiniteFeed();
  initShareComposer();
  initNotificationUI();
  initStoryUI();
  initStoryViewerUI();
  initChatUI();
  initRealtimeChat();
  initWebSocketChat();
  initMobileUX();
}

document.addEventListener("DOMContentLoaded", init);
