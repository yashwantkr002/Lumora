/*
===========================================================
File: static/js/core/toast.js
===========================================================

Purpose

Reusable Toast Notification Engine

Used By

✓ Login
✓ Register
✓ Forgot Password
✓ Profile
✓ Avatar Upload
✓ Cover Upload
✓ Comments
✓ Posts
✓ Notifications
✓ Settings

===========================================================
*/

"use strict";

/* ---------------------------------------------------------
 * Imports
 * ------------------------------------------------------ */

import events from "./events.js";

import { isString, isHTMLElement } from "./utils.js";

/* ---------------------------------------------------------
 * Constants
 * ------------------------------------------------------ */

export const TOAST_TYPES = Object.freeze({
  SUCCESS: "success",

  ERROR: "error",

  WARNING: "warning",

  INFO: "info",
});

export const TOAST_STATUS = Object.freeze({
  HIDDEN: "hidden",

  SHOWING: "showing",

  VISIBLE: "visible",

  HIDING: "hiding",
});

export const DEFAULT_TOAST_OPTIONS = Object.freeze({
  duration: 4000,

  closable: true,

  pauseOnHover: true,

  animationDuration: 300,

  position: "top-right",
});

/* ---------------------------------------------------------
 * Error Classes
 * ------------------------------------------------------ */

export class ToastError extends Error {
  constructor(
    message,

    code = "TOAST_ERROR",
  ) {
    super(message);

    this.name = "ToastError";

    this.code = code;
  }
}

export class InvalidToastMessageError extends ToastError {
  constructor() {
    super(
      "Toast message must be a non-empty string.",

      "INVALID_TOAST_MESSAGE",
    );
  }
}

export class InvalidToastContainerError extends ToastError {
  constructor() {
    super(
      "Toast container must be an HTMLElement.",

      "INVALID_TOAST_CONTAINER",
    );
  }
}

/* ---------------------------------------------------------
 * Validation
 * ------------------------------------------------------ */

function validateMessage(message) {
  if (!isString(message) || message.trim() === "") {
    throw new InvalidToastMessageError();
  }
}

function validateContainer(container) {
  if (container !== null && !isHTMLElement(container)) {
    throw new InvalidToastContainerError();
  }
}

/* ---------------------------------------------------------
 * Toast Class
 * ------------------------------------------------------ */

export class Toast {
  /**
   * @param {string} message
   * @param {string} type
   * @param {Object} options
   */
  constructor(
    message,

    type = TOAST_TYPES.INFO,

    options = {},
  ) {
    validateMessage(message);

    this.message = message;

    this.type = type;

    this.options = {
      ...DEFAULT_TOAST_OPTIONS,

      ...options,
    };

    this.status = TOAST_STATUS.HIDDEN;

    this.element = null;

    this.timer = null;
  }

  /**
   * Is toast visible?
   *
   * @returns {boolean}
   */
  isVisible() {
    return this.status === TOAST_STATUS.VISIBLE;
  }

  /**
   * Create toast element.
   *
   * @returns {HTMLElement}
   */
  createElement() {
    const element = document.createElement("div");

    element.className =
        `toast toast-${this.type}`;

    element.setAttribute(

        "role",

        this.type === TOAST_TYPES.ERROR

            ? "alert"

            : "status",

    );

    element.setAttribute(

        "aria-live",

        this.type === TOAST_TYPES.ERROR

            ? "assertive"

            : "polite",

    );

    element.setAttribute(

        "aria-atomic",

        "true",

    );

    element.innerHTML = `
            <div class="toast-content">
                <span class="toast-message">${this.message}</span>
            </div>
        `;

    if (this.options.closable) {
      const button = document.createElement("button");

      button.type = "button";

      button.className = "toast-close";

      button.setAttribute("aria-label", "Close notification");

      button.innerHTML = "&times;";

      button.addEventListener(
        "click",

        () => this.hide(),
      );

      element.append(button);
    }

    this.element = element;

    return element;
  }

  /**
   * Show toast.
   *
   * @param {HTMLElement} container
   *
   * @returns {Toast}
   */
  show(container) {
    validateContainer(container);

    if (this.isVisible()) {
      return this;
    }

    if (!this.element) {
      this.createElement();
    }

    container.append(this.element);

    requestAnimationFrame(() => {
      this.element.classList.add("show");
    });

    this.status = TOAST_STATUS.VISIBLE;

    events.emit(
      "toast:show",

      this,
    );

    return this;
  }

  /**
   * Hide toast.
   *
   * @returns {Promise<Toast>}
   */
  hide() {

    if (!this.isVisible()) {

      return Promise.resolve(this);

    }

    this.status =
        TOAST_STATUS.HIDING;

    this.element.classList.remove(
      "show",
    );

    events.emit(
      "toast:hide",
      this,
    );

    return new Promise(resolve => {

      setTimeout(() => {

        this.destroy();

        resolve(this);

      }, this.options.animationDuration);

    });

  }

  /**
   * Destroy toast.
   */
  destroy() {
    clearTimeout(this.timer);

    this.element?.remove();

    this.element = null;

    this.status = TOAST_STATUS.HIDDEN;
  }
}
/* ---------------------------------------------------------
 * Toast Manager
 * ------------------------------------------------------ */

export class ToastManager {
  constructor() {
    this.container = null;

    this.toasts = [];
    this.queue = [];
  }

  /**
   * Get or create toast container.
   *
   * @returns {HTMLElement}
   */
  getContainer() {
    if (this.container) {
      return this.container;
    }

    this.container = document.getElementById("toast-container");

    if (!this.container) {
      this.container = document.createElement("div");

      this.container.id = "toast-container";

      this.container.className =

        `toast-container ${

          DEFAULT_TOAST_OPTIONS.position

        }`;

      document.body.append(this.container);
    }

    return this.container;
  }

  /**
   * Show toast.
   *
   * @param {string} message
   * @param {string} type
   * @param {Object} options
   *
   * @returns {Toast}
   */
  show(
    message,

    type,

    options = {},
  ) {
    const toast = new Toast(
      message,

      type,

      options,
    );

    const maxVisible = toast.options.maxVisible;

    if (this.toasts.length >= maxVisible) {
      this.queue.push(toast);

      return toast;
    }

    toast.show(this.getContainer());

    this.toasts.push(toast);

    toast.element?.addEventListener(
      "transitionend",

      () => {
        this.remove(toast);
      },

      {
        once: true,
      },
    );

    return toast;
  }

  /**
   * Success Toast
   */
  success(
    message,

    options = {},
  ) {
    return this.show(
      message,

      TOAST_TYPES.SUCCESS,

      options,
    );
  }

  /**
   * Error Toast
   */
  error(
    message,

    options = {},
  ) {
    return this.show(
      message,

      TOAST_TYPES.ERROR,

      options,
    );
  }

  /**
   * Warning Toast
   */
  warning(
    message,

    options = {},
  ) {
    return this.show(
      message,

      TOAST_TYPES.WARNING,

      options,
    );
  }

  /**
   * Info Toast
   */
  info(
    message,

    options = {},
  ) {
    return this.show(
      message,

      TOAST_TYPES.INFO,

      options,
    );
  }

  /**
   * Number of visible toasts.
   *
   * @returns {number}
   */
  count() {

    return this.toasts.length;

  }

  /**
   * Is queue empty?
   *
   * @returns {boolean}
   */
  isQueueEmpty() {

    return this.queue.length === 0;

  }

  /**
   * Is any toast visible?
   *
   * @returns {boolean}
   */
  hasToasts() {

    return this.toasts.length > 0;

  }

  /**
   * Queue size.
   *
   * @returns {number}
   */
  queueCount() {

    return this.queue.length;

  }

  remove(toast) {

    toast.destroy();

    this.toasts =

      this.toasts.filter(

        item => item !== toast,

      );

    this.processQueue();

  }

  clear() {

    this.toasts.forEach(

      toast => toast.destroy(),

    );

    this.toasts.length = 0;

    this.queue.length = 0;

  }

  /**
   * Process waiting queue.
   */
  processQueue() {

    if (

      this.queue.length === 0

    ) {

      return;

    }

    const next =

      this.queue.shift();

    next.show(

      this.getContainer(),

    );

    this.toasts.push(

      next,

    );

  }
}
/* ---------------------------------------------------------
 * Default Instance
 * ------------------------------------------------------ */

export const toast =

    new ToastManager();

export default toast;
