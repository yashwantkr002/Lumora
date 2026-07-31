import { request } from "../core/http.js";
import { getElement, queryAll } from "../core/dom.js";

function updateLikeButton(button, payload) {
  const icon = button.querySelector("[data-like-icon]");
  const count = button.querySelector("[data-like-count]");
  const total = button.closest(".p-5")?.querySelector("[data-like-total]");

  if (icon) {
    icon.classList.toggle("fa-solid", payload.liked);
    icon.classList.toggle("fa-regular", !payload.liked);
    icon.classList.toggle("text-red-500", payload.liked);
  }

  if (count) {
    count.textContent = payload.likes_count;
  }

  if (total) {
    total.textContent = payload.likes_count;
  }
}

function updateSaveButton(button, payload) {
  const icon = button.querySelector("[data-save-icon]");

  if (icon) {
    icon.classList.toggle("fa-solid", payload.saved);
    icon.classList.toggle("fa-regular", !payload.saved);
  }
}

async function handleToggle(button, url, action) {
  const previousLabel = button.getAttribute("aria-label") ?? action;
  button.setAttribute("aria-label", `${action}ing`);
  button.classList.add("opacity-70");

  try {
    const response = await request(url, {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest" },
    });

    if (!response?.success) {
      throw new Error(response?.message ?? "Request failed");
    }

    if (action === "like") {
      updateLikeButton(button, {
        liked: Boolean(response.liked),
        likes_count: response.likes_count,
      });
    }

    if (action === "save") {
      updateSaveButton(button, {
        saved: Boolean(response.saved),
      });
    }
  } catch (error) {
    console.error(error);
    button.classList.add("animate-pulse");
    window.setTimeout(() => button.classList.remove("animate-pulse"), 600);
  } finally {
    button.classList.remove("opacity-70");
    button.setAttribute("aria-label", previousLabel);
  }
}

function initPostInteractions() {
  const likeButtons = queryAll("[data-like-button]");
  const saveButtons = queryAll("[data-save-button]");

  likeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const url = button.getAttribute("data-url");
      if (!url) return;
      handleToggle(button, url, "like");
    });
  });

  saveButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const url = button.getAttribute("data-url");
      if (!url) return;
      handleToggle(button, url, "save");
    });
  });
}

export function initSocialInteractions() {
  initPostInteractions();
}
