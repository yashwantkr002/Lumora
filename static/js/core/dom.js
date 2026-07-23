/*
===========================================================
File: static/js/core/dom.js
===========================================================

PURPOSE

Reusable DOM utilities for Lumora.

Shared across

- Authentication
- Profile
- Posts
- Stories
- Comments
- Notifications
- Chat

===========================================================
*/

"use strict";

/* --------------------------------------------------------
 * Constants
 * ------------------------------------------------------ */

const ERROR_CLASSES = [
  "border-red-500",
  "focus:border-red-500",
  "focus:ring-red-500",
];

/* --------------------------------------------------------
 * Query Helpers
 * ------------------------------------------------------ */

/**
 * Get element by ID.
 *
 * @param {string} id
 * @returns {HTMLElement|null}
 */
export function getElement(id) {
  return document.getElementById(id);
}

/**
 * Query selector.
 *
 * @template {Element} T
 * @param {string} selector
 * @param {ParentNode} [parent=document]
 * @returns {T|null}
 */
export function query(selector, parent = document) {
  return parent.querySelector(selector);
}

/**
 * Query selector all.
 *
 * @template {Element} T
 * @param {string} selector
 * @param {ParentNode} [parent=document]
 * @returns {T[]}
 */
export function queryAll(selector, parent = document) {
  return [...parent.querySelectorAll(selector)];
}

/* --------------------------------------------------------
 * Visibility Helpers
 * ------------------------------------------------------ */

/**
 * Show an element.
 *
 * @param {HTMLElement|null} element
 */
export function show(element) {
  if (!element) return;

  element.classList.remove("hidden");
}

/**
 * Hide an element.
 *
 * @param {HTMLElement|null} element
 */
export function hide(element) {
  if (!element) return;

  element.classList.add("hidden");
}

/**
 * Toggle visibility.
 *
 * @param {HTMLElement|null} element
 * @param {boolean} [force]
 */
export function toggle(element, force) {
  if (!element) return;

  if (typeof force === "boolean") {
    element.classList.toggle("hidden", !force);

    return;
  }

  element.classList.toggle("hidden");
}

/* --------------------------------------------------------
 * Class Helpers
 * ------------------------------------------------------ */

/**
 * Add classes.
 *
 * @param {Element|null} element
 * @param {...string} classNames
 */
export function addClass(element, ...classNames) {
  if (!element) return;

  element.classList.add(...classNames);
}

/**
 * Remove classes.
 *
 * @param {Element|null} element
 * @param {...string} classNames
 */
export function removeClass(element, ...classNames) {
  if (!element) return;

  element.classList.remove(...classNames);
}

/**
 * Toggle class.
 *
 * @param {Element|null} element
 * @param {string} className
 * @param {boolean} [force]
 */
export function toggleClass(element, className, force) {
  if (!element) return;

  if (typeof force === "boolean") {
    element.classList.toggle(className, force);

    return;
  }

  element.classList.toggle(className);
}

/**
 * Check whether an element has a class.
 *
 * @param {Element|null} element
 * @param {string} className
 * @returns {boolean}
 */
export function hasClass(element, className) {
  if (!element) {
    return false;
  }

  return element.classList.contains(className);
}

/* --------------------------------------------------------
 * Attribute Helpers
 * ------------------------------------------------------ */

/**
 * Set attribute.
 *
 * @param {Element|null} element
 * @param {string} name
 * @param {string} value
 */
export function setAttribute(element, name, value) {
  if (!element) return;

  element.setAttribute(name, value);
}

/**
 * Remove attribute.
 *
 * @param {Element|null} element
 * @param {string} name
 */
export function removeAttribute(element, name) {
  if (!element) return;

  element.removeAttribute(name);
}

/**
 * Get attribute.
 *
 * @param {Element|null} element
 * @param {string} name
 * @returns {string|null}
 */
export function getAttribute(element, name) {
  if (!element) {
    return null;
  }

  return element.getAttribute(name);
}
/* --------------------------------------------------------
 * Text Helpers
 * ------------------------------------------------------ */

/**
 * Set text content.
 *
 * @param {HTMLElement|null} element
 * @param {string} text
 */
export function setText(element, text) {
  if (!element) return;

  element.textContent = text;
}

/**
 * Get text content.
 *
 * @param {HTMLElement|null} element
 * @returns {string}
 */
export function getText(element) {
  if (!element) {
    return "";
  }

  return element.textContent ?? "";
}

/**
 * Set HTML.
 *
 * WARNING:
 * Only use with trusted HTML.
 *
 * @param {HTMLElement|null} element
 * @param {string} html
 */
export function setHTML(element, html) {
  if (!element) return;

  element.innerHTML = html;
}

/**
 * Clear element content.
 *
 * @param {HTMLElement|null} element
 */
export function clear(element) {
  if (!element) return;

  element.replaceChildren();
}

/* --------------------------------------------------------
 * Button Helpers
 * ------------------------------------------------------ */

/**
 * Enable button.
 *
 * @param {HTMLButtonElement|null} button
 */
export function enableButton(button) {
  if (!(button instanceof HTMLButtonElement)) {
    return;
  }

  button.disabled = false;

  button.removeAttribute("aria-disabled");
}

/**
 * Disable button.
 *
 * @param {HTMLButtonElement|null} button
 */
export function disableButton(button) {
  if (!(button instanceof HTMLButtonElement)) {
    return;
  }

  button.disabled = true;

  button.setAttribute("aria-disabled", "true");
}

/* --------------------------------------------------------
 * Focus Helpers
 * ------------------------------------------------------ */

/**
 * Focus an element.
 *
 * @param {HTMLElement|null} element
 */
export function focusField(element) {
  if (!element) return;

  element.focus({
    preventScroll: false,
  });
}

/**
 * Scroll element into view.
 *
 * @param {HTMLElement|null} element
 * @param {ScrollBehavior} [behavior="smooth"]
 */
export function scrollToField(element, behavior = "smooth") {
  if (!element) return;

  element.scrollIntoView({
    behavior,
    block: "center",
    inline: "nearest",
  });
}

/**
 * Focus first invalid field.
 *
 * @param {HTMLFormElement|null} form
 */
export function focusFirstInvalidField(form) {
  if (!form) return;

  const field = form.querySelector(".border-red-500, [aria-invalid='true']");

  if (!(field instanceof HTMLElement)) {
    return;
  }

  scrollToField(field);

  requestAnimationFrame(() => {
    focusField(field);
  });
}

/* --------------------------------------------------------
 * Validation Helpers
 * ------------------------------------------------------ */

/**
 * Get field container.
 *
 * Looks for `.form-field`.
 * Falls back to parentElement.
 *
 * @param {HTMLElement} field
 * @returns {HTMLElement|null}
 */
function getFieldContainer(field) {
  return field.closest(".form-field") ?? field.parentElement;
}

/**
 * Show validation error.
 *
 * @param {HTMLElement|null} field
 * @param {string} message
 */
export function showFieldError(field, message) {
  if (!field) return;

  const container = getFieldContainer(field);

  if (!container) return;

  field.classList.add(...ERROR_CLASSES);

  field.setAttribute("aria-invalid", "true");

  let error = container.querySelector(".field-error");

  if (!error) {
    error = document.createElement("p");

    error.className = "field-error mt-1 text-sm text-red-500";

    container.appendChild(error);
  }

  error.textContent = message;
}

/**
 * Remove validation error.
 *
 * @param {HTMLElement|null} field
 */
export function clearFieldError(field) {
  if (!field) return;

  const container = getFieldContainer(field);

  field.classList.remove(...ERROR_CLASSES);

  field.removeAttribute("aria-invalid");

  if (!container) return;

  container.querySelector(".field-error")?.remove();
}

/**
 * Remove all validation errors.
 *
 * @param {HTMLFormElement|null} form
 */
export function clearFormErrors(form) {
  if (!form) return;

  form.querySelectorAll(".field-error").forEach((error) => error.remove());

  form.querySelectorAll("[aria-invalid='true']").forEach((field) => {
    field.removeAttribute("aria-invalid");

    field.classList.remove(...ERROR_CLASSES);
  });
}

/* --------------------------------------------------------
 * Form Helpers
 * ------------------------------------------------------ */

/**
 * Serialize a form into FormData.
 *
 * @param {HTMLFormElement|null} form
 * @returns {FormData|null}
 */
export function getFormData(form) {
  if (!(form instanceof HTMLFormElement)) {
    return null;
  }

  return new FormData(form);
}

/**
 * Reset a form and clear validation errors.
 *
 * @param {HTMLFormElement|null} form
 */
export function resetForm(form) {
  if (!(form instanceof HTMLFormElement)) {
    return;
  }

  form.reset();

  clearFormErrors(form);
}

/**
 * Check whether a form is valid using
 * native browser validation.
 *
 * @param {HTMLFormElement|null} form
 * @returns {boolean}
 */
export function isFormValid(form) {
  if (!(form instanceof HTMLFormElement)) {
    return false;
  }

  return form.checkValidity();
}

/**
 * Trigger native browser validation UI.
 *
 * @param {HTMLFormElement|null} form
 * @returns {boolean}
 */
export function reportFormValidity(form) {
  if (!(form instanceof HTMLFormElement)) {
    return false;
  }

  return form.reportValidity();
}

/* --------------------------------------------------------
 * Event Helpers
 * ------------------------------------------------------ */

/**
 * Add event listener safely.
 *
 * @param {EventTarget|null} target
 * @param {string} event
 * @param {EventListener} handler
 * @param {boolean|AddEventListenerOptions} [options]
 */
export function on(target, event, handler, options) {
  if (!target) return;

  target.addEventListener(event, handler, options);
}

/**
 * Remove event listener safely.
 *
 * @param {EventTarget|null} target
 * @param {string} event
 * @param {EventListener} handler
 * @param {boolean|EventListenerOptions} [options]
 */
export function off(target, event, handler, options) {
  if (!target) return;

  target.removeEventListener(event, handler, options);
}

/**
 * Add one-time event listener.
 *
 * @param {EventTarget|null} target
 * @param {string} event
 * @param {EventListener} handler
 */
export function once(target, event, handler) {
  if (!target) return;

  target.addEventListener(event, handler, {
    once: true,
  });
}

/* --------------------------------------------------------
 * DOM Ready
 * ------------------------------------------------------ */

/**
 * Run callback after DOM is ready.
 *
 * @param {Function} callback
 */
export function ready(callback) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", callback);

    return;
  }

  callback();
}
