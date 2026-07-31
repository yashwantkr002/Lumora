import { request } from "../core/http.js";
import { getElement, queryAll } from "../core/dom.js";

function parseNextPageUrl(link) {
  const href = link?.getAttribute("href") ?? "";

  if (!href) {
    return null;
  }

  try {
    const url = new URL(href, window.location.origin);
    return `${url.pathname}${url.search}`;
  } catch (error) {
    return null;
  }
}

async function loadNextPage() {
  const container = getElement("feed-posts");
  const sentinel = getElement("feed-sentinel");
  const loader = getElement("feed-loader");

  if (!container || !sentinel) {
    return;
  }

  const nextLink = container.querySelector("[data-next-page]");
  const nextUrl = parseNextPageUrl(nextLink);

  if (!nextUrl || loader?.classList.contains("hidden")) {
    return;
  }

  if (loader) {
    loader.classList.remove("hidden");
  }

  try {
    const html = await request(nextUrl, { method: "GET" });
    const wrapper = document.createElement("div");
    wrapper.innerHTML = html;

    const newPosts = wrapper.querySelectorAll("[data-feed-post]");
    const nextPagination = wrapper.querySelector("[data-next-page]");

    if (newPosts.length) {
      newPosts.forEach((post) => container.appendChild(post));
    }

    if (nextPagination) {
      container.querySelector("[data-pagination]")?.remove();
      container.insertAdjacentHTML("beforeend", nextPagination.outerHTML);
    } else {
      container.querySelector("[data-pagination]")?.remove();
    }
  } catch (error) {
    console.error("Unable to load more posts", error);
  } finally {
    if (loader) {
      loader.classList.add("hidden");
    }
  }
}

export function initInfiniteFeed() {
  const sentinel = getElement("feed-sentinel");

  if (!sentinel) {
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        loadNextPage();
      }
    });
  }, { rootMargin: "600px 0px" });

  observer.observe(sentinel);
}
