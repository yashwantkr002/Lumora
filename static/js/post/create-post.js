/*
===========================================================
File: static/js/posts/create-post.js
===========================================================

Purpose

Coordinate the Create Post workflow.

Responsibilities

✓ Initialize feature modules
✓ Handle form submission
✓ Build FormData
✓ Submit post
✓ Manage loading state
✓ Reset form
✓ Handle success & errors

Does NOT

✗ Validate media
✗ Render previews
✗ Upload implementation
✗ HTTP implementation
✗ Toast implementation

Dependencies

✓ media.js
✓ preview.js
✓ http.js
✓ toast.js
✓ events.js

===========================================================
*/

"use strict";

/* ---------------------------------------------------------
 * Imports
 * ------------------------------------------------------ */

import events from "../core/events.js";
import toast from "../core/toast.js";
import { ready } from "../core/dom.js";

import { MediaManager } from "./media.js";
import { PreviewManager, PREVIEW_EVENTS } from "./preview.js";
import { CreatePostService } from "./create-post.service.js";
/* ---------------------------------------------------------
 * Constants
 * ------------------------------------------------------ */

export const CREATE_POST_EVENTS = Object.freeze({
  SUCCESS: "post:created",

  ERROR: "post:error",
});

const DEFAULT_OPTIONS = Object.freeze({
  form: "#post-form",

  submitButton: "#submit-post-btn",

  submitText: "#submit-text",

  submitSpinner: "#submit-spinner",

  progressWrapper: "#upload-progress-wrapper",

  progressBar: "#upload-progress-bar",

  progressText: "#upload-progress-text",
});

/* ---------------------------------------------------------
 * Error Classes
 * ------------------------------------------------------ */

export class CreatePostError extends Error {
  constructor(message, code = "CREATE_POST_ERROR") {
    super(message);

    this.name = "CreatePostError";

    this.code = code;
  }
}

export class CreatePostInitializationError extends CreatePostError {
  constructor() {
    super(
      "Unable to initialize CreatePostController.",

      "CREATE_POST_INITIALIZATION_ERROR",
    );
  }
}

/* ---------------------------------------------------------
 * Create Post Controller
 * ------------------------------------------------------ */

export class CreatePostController {
  #form;

  #submitButton;

  #submitText;

  #submitSpinner;

  #progressWrapper;

  #progressBar;

  #progressText;

  #mediaManager;

  #previewManager;

  #createPostService;

  #initialized;

  #onSubmit;

  #onPreviewRemove;

  /**
   * @param {Object} [options]
   */
  constructor(options = {}) {
    this.options = {
      ...DEFAULT_OPTIONS,

      ...options,
    };

    this.#form = null;

    this.#submitButton = null;

    this.#submitText = null;

    this.#submitSpinner = null;

    this.#progressWrapper = null;

    this.#progressBar = null;

    this.#progressText = null;

    this.#mediaManager = new MediaManager();

    this.#previewManager = new PreviewManager();

    this.#createPostService = new CreatePostService();

    this.#initialized = false;

    this.#onSubmit = this.#handleSubmit.bind(this);

    this.#onPreviewRemove = this.#handlePreviewRemove.bind(this);
  }
  /* ---------------------------------------------------------
   * Initialization
   * ------------------------------------------------------ */

  /**
   * Initialize controller.
   *
   * @returns {CreatePostController}
   */
  initialize() {
    if (this.#initialized) {
      return this;
    }

    this.#resolveElements();

    this.#mediaManager.initialize();

    this.#previewManager.initialize();

    this.#bindEvents();

    this.#initialized = true;

    return this;
  }

  /**
   * Destroy controller.
   */
  destroy() {
    if (!this.#initialized) {
      return;
    }

    this.#unbindEvents();

    this.#mediaManager.destroy();

    this.#previewManager.destroy();

    this.#initialized = false;
  }

  /* ---------------------------------------------------------
   * Private Helpers
   * ------------------------------------------------------ */

  /**
   * Resolve DOM elements.
   *
   * @private
   */
  #resolveElements() {
    this.#form = document.querySelector(this.options.form);

    this.#submitButton = document.querySelector(this.options.submitButton);

    this.#submitText = document.querySelector(this.options.submitText);

    this.#submitSpinner = document.querySelector(this.options.submitSpinner);

    this.#progressWrapper = document.querySelector(
      this.options.progressWrapper,
    );

    this.#progressBar = document.querySelector(this.options.progressBar);

    this.#progressText = document.querySelector(this.options.progressText);

    if (!this.#form) {
      throw new CreatePostInitializationError();
    }
  }

  /**
   * Bind events.
   *
   * @private
   */
  #bindEvents() {
    this.#form.addEventListener(
      "submit",

      this.#onSubmit,
    );

    events.on(
      PREVIEW_EVENTS.REMOVE,

      this.#onPreviewRemove,
    );
  }

  /**
   * Remove event listeners.
   *
   * @private
   */
  #unbindEvents() {
    this.#form?.removeEventListener(
      "submit",

      this.#onSubmit,
    );

    events.off(
      PREVIEW_EVENTS.REMOVE,

      this.#onPreviewRemove,
    );
  }

  /**
   * Handle preview remove event.
   *
   * @private
   *
   * @param {{index:number}} payload
   */
  #handlePreviewRemove(payload) {
    this.#mediaManager.remove(payload.index);
  }
  /* ---------------------------------------------------------
   * Form Submission
   * ------------------------------------------------------ */

  /**
   * Handle form submission.
   *
   * @private
   *
   * @param {SubmitEvent} event
   */
  async #handleSubmit(event) {
    event.preventDefault();

    try {
      this.#toggleLoading(true);

      const formData = this.#buildFormData();

      const response = await this.#createPostService.create(formData, {
        timeout: 60000,
      });

      this.#handleSuccess(response);
    } catch (error) {
      this.#handleError(error);
    } finally {
      this.#toggleLoading(false);
    }
  }

  /**
   * Build multipart FormData.
   *
   * @private
   *
   * @returns {FormData}
   */
  #buildFormData() {
    const formData = new FormData(this.#form);

    this.#mediaManager.getFiles().forEach((file) => {
      formData.append("media", file);
    });

    return formData;
  }

  /**
   * Toggle loading state.
   *
   * @private
   *
   * @param {boolean} loading
   */
  #toggleLoading(loading) {
    this.#submitButton.disabled = loading;

    this.#submitSpinner.hidden = !loading;

    this.#submitText.hidden = loading;

    this.#progressWrapper.hidden = !loading;
  }
  /* ---------------------------------------------------------
 * Response Handlers
 * ------------------------------------------------------ */

/**
 * Handle successful post creation.
 *
 * @private
 *
 * @param {*} response
 */
#handleSuccess(response) {

    toast.success("Post created successfully.");

    this.#resetForm();

    events.emit(
        CREATE_POST_EVENTS.SUCCESS,
        response,
    );

}

/**
 * Handle request errors.
 *
 * @private
 *
 * @param {Error} error
 */
#handleError(error) {

    const message =
        error?.data?.message ??
        error?.message ??
        "Unable to create post.";

    toast.error(message);

    events.emit(
        CREATE_POST_EVENTS.ERROR,
        {
            error,
            message,
        },
    );

}

/**
 * Reset create post form.
 *
 * @private
 */
#resetForm() {

    this.#form.reset();

    this.#mediaManager.clear();

    this.#previewManager.clear().hide();

    this.#progressBar.value = 0;

    this.#progressText.textContent = "0%";

    this.#progressWrapper.hidden = true;

}
}

ready(() => {
  new CreatePostController().initialize();
});
