/*
===========================================================
File: static/js/posts/preview.js
===========================================================

Purpose

Render media previews for the Create/Edit Post form.

Responsibilities

✓ Listen to media events
✓ Render image previews
✓ Render video preview
✓ Manage Object URLs
✓ Cleanup Object URLs
✓ Remove preview cards

Does NOT

✗ Validate media
✗ Upload files
✗ Submit forms
✗ Make HTTP requests
✗ Own media state

Dependencies

✓ events.js
✓ media.js

===========================================================
*/

"use strict";

/* ---------------------------------------------------------
 * Imports
 * ------------------------------------------------------ */

import events from "../core/events.js";

import { MEDIA_EVENTS } from "./media.js";

/* ---------------------------------------------------------
 * Constants
 * ------------------------------------------------------ */

const DEFAULT_OPTIONS = Object.freeze({
  container: "#media-preview",
});

export const PREVIEW_EVENTS = Object.freeze({
  REMOVE: "preview:remove",
});

const PREVIEW_CLASS = Object.freeze({
  CONTAINER: "media-preview",

  HEADER: "preview-header",

  CARD: "preview-card",

  IMAGE: "preview-image",

  VIDEO: "preview-video",

  REMOVE_BUTTON: "preview-remove",

  EMPTY: "preview-empty",
});

/* ---------------------------------------------------------
 * Error Classes
 * ------------------------------------------------------ */

export class PreviewError extends Error {
  constructor(message, code = "PREVIEW_ERROR") {
    super(message);

    this.name = "PreviewError";

    this.code = code;
  }
}

export class PreviewInitializationError extends PreviewError {
  constructor() {
    super(
      "Unable to initialize PreviewManager.",

      "PREVIEW_INITIALIZATION_ERROR",
    );
  }
}

export class InvalidPreviewContainerError extends PreviewError {
  constructor() {
    super(
      "Preview container not found.",

      "INVALID_PREVIEW_CONTAINER",
    );
  }
}

/* ---------------------------------------------------------
 * Preview Manager
 * ------------------------------------------------------ */

export class PreviewManager {
  #container;

  #objectUrls;

  #cards;

  #initialized;

  #onSelected;

  #onRemoved;

  #onCleared;

  /**
   * @param {Object} [options]
   * @param {string|HTMLElement} [options.container]
   */
  constructor(options = {}) {
    this.options = {
      ...DEFAULT_OPTIONS,

      ...options,
    };

    this.#container = null;

    this.#objectUrls = new Map();

    this.#cards = new Map();

    this.#initialized = false;

    this.#onSelected = this.#handleSelected.bind(this);

    this.#onRemoved = this.#handleRemoved.bind(this);

    this.#onCleared = this.#handleCleared.bind(this);
  }
  /* ---------------------------------------------------------
   * Initialization
   * ------------------------------------------------------ */

  /**
   * Initialize preview manager.
   *
   * @returns {PreviewManager}
   *
   * @throws {InvalidPreviewContainerError}
   */
  initialize() {
    if (this.#initialized) {
      return this;
    }

    this.#resolveContainer();

    this.#bindEvents();

    this.#createEmptyState();

    this.#initialized = true;

    return this;
  }

  /**
   * Destroy preview manager.
   *
   * @returns {void}
   */

  /* ---------------------------------------------------------
   * Private Helpers
   * ------------------------------------------------------ */

  /**
   * Resolve preview container.
   *
   * @private
   *
   * @throws {InvalidPreviewContainerError}
   */
  #resolveContainer() {
    const { container } = this.options;

    if (container instanceof HTMLElement) {
      this.#container = container;
    } else if (typeof container === "string") {
      this.#container = document.querySelector(container);
    }

    if (!(this.#container instanceof HTMLElement)) {
      throw new InvalidPreviewContainerError();
    }
  }

  /**
   * Subscribe to media events.
   *
   * @private
   */
  #bindEvents() {
    events.on(MEDIA_EVENTS.SELECTED, this.#onSelected);

    events.on(MEDIA_EVENTS.REMOVED, this.#onRemoved);

    events.on(MEDIA_EVENTS.CLEARED, this.#onCleared);
  }

  /**
   * Unsubscribe from media events.
   *
   * @private
   */
  #unbindEvents() {
    events.off(MEDIA_EVENTS.SELECTED, this.#onSelected);

    events.off(MEDIA_EVENTS.REMOVED, this.#onRemoved);

    events.off(MEDIA_EVENTS.CLEARED, this.#onCleared);
  }

  /* ---------------------------------------------------------
   * Event Handlers
   * ------------------------------------------------------ */

  /**
   * Handle media:selected.
   *
   * @private
   *
   * @param {Object} payload
   */
  #handleSelected(payload) {
    this.render(payload.files);
  }

  /**
   * Handle media:removed.
   *
   * @private
   *
   * @param {Object} payload
   */
  #handleRemoved(payload) {
    if (payload?.removedFile) {
      this.#removeCard(payload.removedFile);

      return;
    }

    this.render(payload.files);
  }

  /**
   * Handle media:cleared.
   *
   * @private
   */
  #handleCleared() {
    this.clear();
  }
  /* ---------------------------------------------------------
   * Public API
   * ------------------------------------------------------ */

  /**
   * Render media previews.
   *
   * @param {File[]} files
   *
   * @returns {void}
   */
  render(files = []) {
    this.clear();

    this.#container.classList.remove("hidden");

    this.#container.appendChild(this.#createHeader(files.length));

    if (files.length === 0) {
      this.#container.appendChild(this.#createEmptyState());

      return;
    }

    const fragment = document.createDocumentFragment();

    files.forEach((file, index) => {
      const card = this.#createCard(file, index);

      fragment.appendChild(card);
    });

    this.#container.appendChild(fragment);
  }

  /* ---------------------------------------------------------
   * DOM Builders
   * ------------------------------------------------------ */

  /**
   * Create preview card.
   *
   * @private
   *
   * @param {File} file
   * @param {number} index
   *
   * @returns {HTMLDivElement}
   */
  #createCard(file, index) {
    const card = document.createElement("div");

    card.className = PREVIEW_CLASS.CARD;

    let media;

    if (file.type.startsWith("image/")) {
      media = this.#createImage(file);
    } else {
      media = this.#createVideo(file);
    }

    const removeButton = this.#createRemoveButton(index);

    card.appendChild(media);

    card.appendChild(removeButton);

    this.#cards.set(file, card);

    return card;
  }

  /**
   * Create image preview.
   *
   * @private
   *
   * @param {File} file
   *
   * @returns {HTMLImageElement}
   */
  #createImage(file) {
    const image = document.createElement("img");

    const objectUrl = URL.createObjectURL(file);

    image.src = objectUrl;

    image.alt = file.name;

    image.loading = "lazy";

    image.className = PREVIEW_CLASS.IMAGE;

    this.#objectUrls.set(file, objectUrl);

    return image;
  }

  /**
   * Create video preview.
   *
   * @private
   *
   * @param {File} file
   *
   * @returns {HTMLVideoElement}
   */
  #createVideo(file) {
    const video = document.createElement("video");

    const objectUrl = URL.createObjectURL(file);

    video.src = objectUrl;

    video.controls = true;

    video.preload = "metadata";

    video.className = PREVIEW_CLASS.VIDEO;

    this.#objectUrls.set(file, objectUrl);

    return video;
  }

  /**
   * Create remove button.
   *
   * @private
   *
   * @param {number} index
   *
   * @returns {HTMLButtonElement}
   */
  #createRemoveButton(index) {
    const button = document.createElement("button");

    button.type = "button";

    button.className = PREVIEW_CLASS.REMOVE_BUTTON;

    button.dataset.index = String(index);

    button.setAttribute("aria-label", "Remove media");

    button.textContent = "×";

    button.addEventListener("click", () => {
      events.emit(PREVIEW_EVENTS.REMOVE, {
        index,
      });
    });

    return button;
  }

  /**
   * Create empty state.
   *
   * @private
   *
   * @returns {HTMLDivElement}
   */
  #createEmptyState() {
    const empty = document.createElement("div");

    empty.className = PREVIEW_CLASS.EMPTY;

    empty.textContent = "No items selected.";

    return empty;
  }

  /**
   * Create preview header.
   *
   * @private
   *
   * @param {number} count
   * @returns {HTMLHeadingElement}
   */
  #createHeader(count) {
    const heading = document.createElement("h2");

    heading.className = PREVIEW_CLASS.HEADER;

    if (count === 0) {
      heading.textContent = "Selected items";
    } else {
      heading.textContent = `${count} selected item${count === 1 ? "" : "s"}`;
    }

    return heading;
  }
  /* ---------------------------------------------------------
   * Public API
   * ------------------------------------------------------ */

  /**
   * Hide the preview container.
   *
   * @returns {PreviewManager}
   */
  hide() {
    if (this.#container) {
      this.#container.classList.add("hidden");
    }

    return this;
  }

  /**
   * Clear all rendered previews.
   *
   * @returns {PreviewManager}
   */
  clear() {
    this.#revokeObjectURLs();

    this.#cards.clear();

    if (this.#container) {
      this.#container.replaceChildren();
    }

    return this;
  }

  /* ---------------------------------------------------------
   * Cleanup Helpers
   * ------------------------------------------------------ */

  /**
   * Remove a preview card.
   *
   * @private
   *
   * @param {File} file
   */
  #removeCard(file) {
    const card = this.#cards.get(file);

    if (!card) {
      return;
    }

    card.remove();

    this.#cards.delete(file);

    const objectUrl = this.#objectUrls.get(file);

    if (objectUrl) {
      URL.revokeObjectURL(objectUrl);

      this.#objectUrls.delete(file);
    }

    if (this.#cards.size === 0) {
      this.#container.appendChild(this.#createEmptyState());
    }
  }

  /**
   * Revoke every Object URL.
   *
   * @private
   */
  #revokeObjectURLs() {
    for (const objectUrl of this.#objectUrls.values()) {
      URL.revokeObjectURL(objectUrl);
    }

    this.#objectUrls.clear();
  }

  /* ---------------------------------------------------------
   * Lifecycle
   * ------------------------------------------------------ */

  /**
   * Destroy preview manager.
   *
   * @returns {void}
   */
  destroy() {
    if (!this.#initialized) {
      return;
    }

    this.#unbindEvents();

    this.clear();

    this.#container = null;

    this.#initialized = false;
  }
}
