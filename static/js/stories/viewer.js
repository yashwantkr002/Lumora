import { getElement } from "../core/dom.js";

function initStoryViewer() {
  const progress = getElement("story-progress");
  const viewer = getElement("story-viewer");
  const media = getElement("story-media");

  if (!progress || !viewer) {
    return;
  }

  let width = 0;
  const timer = window.setInterval(() => {
    width += 1;
    progress.style.width = `${width}%`;

    if (width >= 100) {
      window.clearInterval(timer);
      const nextStoryLink = viewer.getAttribute("data-next-story-url");

      if (nextStoryLink) {
        window.location.href = nextStoryLink;
      }
    }
  }, 100);

  media?.addEventListener("mouseenter", () => {
    progress.classList.add("bg-amber-400");
  });

  media?.addEventListener("mouseleave", () => {
    progress.classList.remove("bg-amber-400");
  });
}

export function initStoryViewerUI() {
  initStoryViewer();
}
