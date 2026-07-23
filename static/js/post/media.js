/*
===========================================================
File: static/js/posts/media.js
===========================================================

Purpose

Media selection and state management for Create/Edit Post.

Responsibilities

✓ Handle file input changes
✓ Validate media selection
✓ Maintain selected media state
✓ Emit media events
✓ Expose public API

Does NOT

✗ Render previews
✗ Upload files
✗ Submit forms
✗ Perform HTTP requests

Dependencies

✓ config.js
✓ events.js
✓ toast.js

Used By

✓ create-post.js
✓ preview.js

===========================================================
*/

"use strict";

/* ---------------------------------------------------------
 * Imports
 * ------------------------------------------------------ */

import { AppConfig } from "../core/config.js";

import events from "../core/events.js";

import toast from "../core/toast.js";

/* ---------------------------------------------------------
 * Constants
 * ------------------------------------------------------ */

export const MEDIA_EVENTS = Object.freeze({
  SELECTED: "media:selected",

  REMOVED: "media:removed",

  CLEARED: "media:cleared",

  ERROR: "media:error",
});

const DEFAULT_OPTIONS = Object.freeze({
  input: "#media",
});

/* ---------------------------------------------------------
 * Error Classes
 * ------------------------------------------------------ */

export class MediaError extends Error {
  constructor(message, code = "MEDIA_ERROR") {
    super(message);

    this.name = "MediaError";

    this.code = code;
  }
}

export class MediaInitializationError extends MediaError {
  constructor() {
    super(
      "Unable to initialize MediaManager.",

      "MEDIA_INITIALIZATION_ERROR",
    );
  }
}

export class InvalidMediaInputError extends MediaError {
  constructor() {
    super(
      "Media input element not found.",

      "INVALID_MEDIA_INPUT",
    );
  }
}

/* ---------------------------------------------------------
 * Media Manager
 * ------------------------------------------------------ */

export class MediaManager {
  #input;

  #files;

  #images;

  #videos;

  #initialized;

  #handleChange;

  /**
   * @param {Object} [options]
   * @param {string|HTMLInputElement} [options.input]
   */
  constructor(options = {}) {
    this.options = {
      ...DEFAULT_OPTIONS,

      ...options,
    };

    this.#input = null;

    this.#files = [];

    this.#images = [];

    this.#videos = [];

    this.#initialized = false;

    this.#handleChange = this.#onFileChange.bind(this);
  }
  /* ---------------------------------------------------------
   * Initialization
   * ------------------------------------------------------ */

  /**
   * Initialize media manager.
   *
   * @returns {MediaManager}
   *
   * @throws {InvalidMediaInputError}
   */
  initialize() {
    if (this.#initialized) {
      return this;
    }

    this.#resolveInput();

    this.#bindEvents();

    this.#initialized = true;

    return this;
  }

  /**
   * Destroy media manager.
   *
   * @returns {void}
   */
  destroy() {
    if (!this.#initialized) {
      return;
    }

    this.#unbindEvents();

    this.clear();

    this.#initialized = false;
  }

  /* ---------------------------------------------------------
   * Private Helpers
   * ------------------------------------------------------ */

  /**
   * Resolve file input element.
   *
   * @private
   *
   * @throws {InvalidMediaInputError}
   */
  #resolveInput() {
    const { input } = this.options;

    if (input instanceof HTMLInputElement) {
      this.#input = input;
    } else if (typeof input === "string") {
      this.#input = document.querySelector(input);
    }

    if (!(this.#input instanceof HTMLInputElement)) {
      throw new InvalidMediaInputError();
    }

    if (this.#input.type !== "file") {
      throw new InvalidMediaInputError();
    }
  }

  /**
   * Bind DOM events.
   *
   * @private
   */
  #bindEvents() {
    this.#input.addEventListener(
      "change",

      this.#handleChange,
    );
  }

  /**
   * Remove DOM events.
   *
   * @private
   */
  #unbindEvents() {
    this.#input?.removeEventListener(
      "change",

      this.#handleChange,
    );
  }

  /**
   * Reset file input.
   *
   * Allows selecting the same file again.
   *
   * @private
   */
  #resetInput() {
    if (!this.#input) {
      return;
    }

    this.#input.value = "";
  }

  /**
   * Handle native file input change.
   *
   * @private
   *
   * @param {Event} event
   */
  #onFileChange(event) {
    const input = /** @type {HTMLInputElement} */ (event.currentTarget);

    const files = Array.from(input.files ?? []);

    this.addFiles(files);
  }
  /* ---------------------------------------------------------
   * Public API
   * ------------------------------------------------------ */

  /**
   * Add files to media manager.
   *
   * @param {File[]|FileList} files
   *
   * @returns {boolean}
   */
  addFiles(files) {
    const candidates = Array.from(files ?? []);

    const uniqueNewFiles = candidates.filter(
      (file, index, list) =>
        !this.#isDuplicate(file) &&
        list.findIndex(
          (candidate) =>
            candidate.name === file.name &&
            candidate.size === file.size &&
            candidate.lastModified === file.lastModified,
        ) === index,
    );

    if (uniqueNewFiles.length === 0) {
      this.#resetInput();

      return false;
    }

    const combinedFiles = [...this.#files, ...uniqueNewFiles];

    try {
      this.#validateSelection(combinedFiles);

      this.#files = combinedFiles;

      this.#images = this.#files.filter((file) =>
        AppConfig.ACCEPTED_IMAGE_TYPES.includes(file.type),
      );

      this.#videos = this.#files.filter((file) =>
        AppConfig.ACCEPTED_VIDEO_TYPES.includes(file.type),
      );

      this.#emitSelected();

      return true;
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Unable to process selected media.";

      toast.error(message);

      events.emit(MEDIA_EVENTS.ERROR, { message });

      this.#resetInput();

      return false;
    }
  }

  /* ---------------------------------------------------------
   * Validation
   * ------------------------------------------------------ */

  /**
   * Validate selected files.
   *
   * @private
   *
   * @param {File[]} files
   */
  #validateSelection(files) {
    this.#validateMime(files);

    this.#validateMixedMedia(files);

    this.#validateLimits(files);
  }

  /**
   * Validate MIME types.
   *
   * @private
   *
   * @param {File[]} files
   */
  #validateMime(files) {
    for (const file of files) {
      const valid =
        AppConfig.ACCEPTED_IMAGE_TYPES.includes(file.type) ||
        AppConfig.ACCEPTED_VIDEO_TYPES.includes(file.type);

      if (!valid) {
        throw new MediaError(
          `Unsupported file type: ${file.type}`,

          "INVALID_MEDIA_TYPE",
        );
      }
    }
  }

  /**
   * Prevent mixing images and videos.
   *
   * @private
   *
   * @param {File[]} files
   */
  #validateMixedMedia(files) {
    const imageCount = files.filter((file) =>
      AppConfig.ACCEPTED_IMAGE_TYPES.includes(file.type),
    ).length;

    const videoCount = files.filter((file) =>
      AppConfig.ACCEPTED_VIDEO_TYPES.includes(file.type),
    ).length;

    if (imageCount > 0 && videoCount > 0) {
      throw new MediaError(
        "Images and videos cannot be uploaded together.",

        "MIXED_MEDIA",
      );
    }
  }

  /**
   * Validate upload limits.
   *
   * @private
   *
   * @param {File[]} files
   */
  #validateLimits(files) {
    const imageCount = files.filter((file) =>
      AppConfig.ACCEPTED_IMAGE_TYPES.includes(file.type),
    ).length;

    const videoCount = files.filter((file) =>
      AppConfig.ACCEPTED_VIDEO_TYPES.includes(file.type),
    ).length;

    if (imageCount > AppConfig.MAX_UPLOAD_FILES) {
      throw new MediaError(
        `Maximum ${AppConfig.MAX_UPLOAD_FILES} images allowed.`,

        "MAX_IMAGES_EXCEEDED",
      );
    }

    if (videoCount > AppConfig.MAX_VIDEO_FILES) {
      throw new MediaError(
        "Only one video can be uploaded.",

        "MAX_VIDEO_EXCEEDED",
      );
    }
  }
  /* ---------------------------------------------------------
   * Public API
   * ------------------------------------------------------ */

  /**
   * Remove a selected file.
   *
   * @param {number} index
   *
   * @returns {boolean}
   */
  remove(index) {
    if (!Number.isInteger(index)) {
      return false;
    }

    if (index < 0 || index >= this.#files.length) {
      return false;
    }

    const [removedFile] = this.#files.splice(index, 1);

    this.#images = this.#files.filter((file) =>
      AppConfig.ACCEPTED_IMAGE_TYPES.includes(file.type),
    );

    this.#videos = this.#files.filter((file) =>
      AppConfig.ACCEPTED_VIDEO_TYPES.includes(file.type),
    );

    this.#emitRemoved(removedFile, index);

    if (this.#files.length === 0) {
      this.#emitCleared();
    } else {
      this.#emitSelected();
    }

    this.#resetInput();

    return true;
  }

  /**
   * Clear all selected files.
   *
   * @returns {MediaManager}
   */
  clear() {
    this.#files.length = 0;

    this.#images.length = 0;

    this.#videos.length = 0;

    this.#resetInput();

    this.#emitCleared();

    return this;
  }

  /**
   * Get selected files.
   *
   * Returns a defensive copy.
   *
   * @returns {File[]}
   */
  getFiles() {
    return [...this.#files];
  }

  /**
   * Get image files.
   *
   * @returns {File[]}
   */
  getImages() {
    return [...this.#images];
  }

  /**
   * Get video files.
   *
   * @returns {File[]}
   */
  getVideos() {
    return [...this.#videos];
  }

  /**
   * Number of selected files.
   *
   * @returns {number}
   */
  getFileCount() {
    return this.#files.length;
  }

  /**
   * Whether any media exists.
   *
   * @returns {boolean}
   */
  hasFiles() {
    return this.#files.length > 0;
  }

  /* ---------------------------------------------------------
   * Event Emitters
   * ------------------------------------------------------ */

  /**
   * Emit media:selected.
   *
   * @private
   */
  #emitSelected() {
    events.emit(
      MEDIA_EVENTS.SELECTED,
      Object.freeze({
        files: this.getFiles(),
        images: this.getImages(),
        videos: this.getVideos(),
      }),
    );
  }

  /**
   * Emit media:removed.
   *
   * @private
   *
   * @param {File} removedFile
   * @param {number} index
   */
  #emitRemoved(removedFile, index) {
    events.emit(
      MEDIA_EVENTS.REMOVED,

      {
        removedFile,

        index,

        files: this.getFiles(),

        images: this.getImages(),

        videos: this.getVideos(),
      },
    );
  }

  /**
   * Emit media:cleared.
   *
   * @private
   */
  #emitCleared() {
    events.emit(
      MEDIA_EVENTS.CLEARED,

      {
        files: [],

        images: [],

        videos: [],
      },
    );
  }
  #isDuplicate(file) {
    return this.#files.some(
      (existing) =>
        existing.name === file.name &&
        existing.size === file.size &&
        existing.lastModified === file.lastModified,
    );
  }
}
