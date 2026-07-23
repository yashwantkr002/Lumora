/*
===========================================================
File: static/js/core/utils.js
===========================================================

PURPOSE

Reusable utility functions for Lumora.

Used By

- Authentication
- Profile
- Posts
- Comments
- Stories
- Chat
- Notifications

===========================================================
*/

"use strict";

/* --------------------------------------------------------
 * Timing Helpers
 * ------------------------------------------------------ */

/**
 * Debounce function.
 *
 * @template {(...args: any[]) => void} T
 * @param {T} callback
 * @param {number} [delay=300]
 * @returns {T}
 */
export function debounce(callback, delay = 300) {
  let timeoutId;

  return /** @type {T} */ (
    (...args) => {
      clearTimeout(timeoutId);

      timeoutId = window.setTimeout(() => callback(...args), delay);
    }
  );
}

/**
 * Throttle function.
 *
 * @template {(...args: any[]) => void} T
 * @param {T} callback
 * @param {number} [delay=300]
 * @returns {T}
 */
export function throttle(callback, delay = 300) {
  let waiting = false;

  return /** @type {T} */ (
    (...args) => {
      if (waiting) {
        return;
      }

      callback(...args);

      waiting = true;

      window.setTimeout(() => {
        waiting = false;
      }, delay);
    }
  );
}

/**
 * Sleep helper.
 *
 * @param {number} milliseconds
 * @returns {Promise<void>}
 */
export function sleep(milliseconds) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, milliseconds);
  });
}

/* --------------------------------------------------------
 * String Helpers
 * ------------------------------------------------------ */

/**
 * Trim safely.
 *
 * @param {*} value
 * @returns {string}
 */
export function trim(value) {
  return String(value ?? "").trim();
}

/**
 * Check empty value.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isEmpty(value) {
  return trim(value) === "";
}

/**
 * Capitalize first letter.
 *
 * @param {string} value
 * @returns {string}
 */
export function capitalize(value) {
  if (!value) {
    return "";
  }

  return value.charAt(0).toUpperCase() + value.slice(1);
}

/**
 * Convert string to title case.
 *
 * @param {string} value
 * @returns {string}
 */
export function titleCase(value) {
  return trim(value).split(/\s+/).map(capitalize).join(" ");
}

/**
 * Escape HTML.
 *
 * @param {string} value
 * @returns {string}
 */
export function escapeHTML(value) {
  const div = document.createElement("div");

  div.textContent = value;

  return div.innerHTML;
}

/* --------------------------------------------------------
 * Browser Helpers
 * ------------------------------------------------------ */

/**
 * Check mobile device.
 *
 * @returns {boolean}
 */
export function isMobile() {
  return window.innerWidth < 768;
}

/**
 * Check touch device.
 *
 * @returns {boolean}
 */
export function isTouchDevice() {
  return "ontouchstart" in window || navigator.maxTouchPoints > 0;
}

/* --------------------------------------------------------
 * Clipboard Helpers
 * ------------------------------------------------------ */

/**
 * Copy text to clipboard.
 *
 * @param {string} text
 * @returns {Promise<boolean>}
 */
export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);

    return true;
  } catch {
    return false;
  }
}

/* --------------------------------------------------------
 * ID Helpers
 * ------------------------------------------------------ */

/**
 * Generate UUID.
 *
 * @returns {string}
 */
export function generateUUID() {
  return crypto.randomUUID();
}

/**
 * Generate random string.
 *
 * @param {number} [length=8]
 * @returns {string}
 */
export function randomString(length = 8) {
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  return Array.from({ length }, () =>
    characters.charAt(Math.floor(Math.random() * characters.length)),
  ).join("");
}

/* --------------------------------------------------------
 * Date Helpers
 * ------------------------------------------------------ */

/**
 * Format date.
 *
 * @param {Date|string|number} date
 * @param {string} [locale="en-IN"]
 * @returns {string}
 */
export function formatDate(date, locale = "en-IN") {
  return new Intl.DateTimeFormat(locale, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(date));
}

/**
 * Format relative time.
 *
 * @param {Date|string|number} date
 * @returns {string}
 */
export function timeAgo(date) {
  const formatter = new Intl.RelativeTimeFormat("en", {
    numeric: "auto",
  });

  const seconds = Math.floor((new Date(date).getTime() - Date.now()) / 1000);

  const intervals = [
    ["year", 31536000],
    ["month", 2592000],
    ["week", 604800],
    ["day", 86400],
    ["hour", 3600],
    ["minute", 60],
  ];

  for (const [unit, value] of intervals) {
    if (Math.abs(seconds) >= value) {
      return formatter.format(Math.floor(seconds / value), unit);
    }
  }

  return formatter.format(seconds, "second");
}

/* --------------------------------------------------------
 * Number Helpers
 * ------------------------------------------------------ */

/**
 * Clamp number.
 *
 * @param {number} value
 * @param {number} min
 * @param {number} max
 * @returns {number}
 */
export function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

/**
 * Format number.
 *
 * @param {number} value
 * @param {string} [locale="en-IN"]
 * @returns {string}
 */
export function formatNumber(value, locale = "en-IN") {
  return new Intl.NumberFormat(locale).format(value);
}

/* --------------------------------------------------------
 * URL Helpers
 * ------------------------------------------------------ */

/**
 * Get query parameter.
 *
 * @param {string} name
 * @returns {string|null}
 */
export function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

/**
 * Redirect to another page.
 *
 * @param {string} url
 */
export function redirect(url) {
  window.location.assign(url);
}
/* --------------------------------------------------------
 * Loading Helpers
 * ------------------------------------------------------ */

/**
 * Set button loading state.
 *
 * @param {HTMLButtonElement|null} button
 * @param {string} [loadingText="Loading..."]
 */
export function setButtonLoading(button, loadingText = "Loading...") {
  if (!(button instanceof HTMLButtonElement)) {
    return;
  }

  if (!button.dataset.originalText) {
    button.dataset.originalText = button.innerHTML;
  }

  button.disabled = true;

  button.setAttribute("aria-busy", "true");

  button.innerHTML = `
        <span class="inline-flex items-center gap-2">
            <svg
                class="h-4 w-4 animate-spin"
                viewBox="0 0 24 24"
                fill="none"
                aria-hidden="true"
            >
                <circle
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="3"
                    opacity=".25"
                ></circle>

                <path
                    d="M22 12a10 10 0 0 1-10 10"
                    stroke="currentColor"
                    stroke-width="3"
                ></path>
            </svg>

            ${escapeHTML(loadingText)}
        </span>
    `;
}

/**
 * Reset button loading state.
 *
 * @param {HTMLButtonElement|null} button
 */
export function resetButtonLoading(button) {
  if (!(button instanceof HTMLButtonElement)) {
    return;
  }

  button.disabled = false;

  button.removeAttribute("aria-busy");

  if (button.dataset.originalText) {
    button.innerHTML = button.dataset.originalText;

    delete button.dataset.originalText;
  }
}

/* --------------------------------------------------------
 * Object Helpers
 * ------------------------------------------------------ */

/**
 * Deep clone.
 *
 * @template T
 * @param {T} value
 * @returns {T}
 */
export function deepClone(value) {
  return structuredClone(value);
}

/**
 * Deep equality.
 *
 * @param {*} a
 * @param {*} b
 * @returns {boolean}
 */
export function isEqual(a, b) {
  return JSON.stringify(a) === JSON.stringify(b);
}

/* --------------------------------------------------------
 * Async Helpers
 * ------------------------------------------------------ */

/**
 * Execute async function safely.
 *
 * @template T
 * @param {() => Promise<T>} callback
 * @returns {Promise<T|null>}
 */
export async function safeAsync(callback) {
    try {
        return {
            success: true,
            data: await callback(),
            error: null,
        };
    } catch (error) {
        return {
            success: false,
            data: null,
            error,
        };
    }
}
export function isPromise(value) {
    return value instanceof Promise;
}

export function isBoolean(value) {
    return typeof value === "boolean";
}

export function isArray(value) {
    return Array.isArray(value);
}

export function isHTMLElement(value) {
    return value instanceof HTMLElement;
}

export function isCanvasContext(value) {
    return value instanceof CanvasRenderingContext2D;
}
export function revokeObjectURL(url) {

    if (url) {
        URL.revokeObjectURL(url);
    }

}

export function createObjectURL(file) {

    return URL.createObjectURL(file);

}
export function round(value, precision = 2) {

    const factor = 10 ** precision;

    return Math.round(value * factor) / factor;

}
export function bytesToMB(bytes) {

    return bytes / 1024 / 1024;

}

export function mbToBytes(mb) {

    return mb * 1024 * 1024;

}
export function getFileExtension(file) {

    if (!isFile(file)) {
        return "";
    }

    return file.name.split(".").pop()?.toLowerCase() ?? "";

}

export function isMimeType(file, allowedTypes) {

    return allowedTypes.includes(file.type);

}

/* --------------------------------------------------------
 * Type Helpers
 * ------------------------------------------------------ */

/**
 * Check number.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isNumber(value) {
    return typeof value === "number" && Number.isFinite(value);
}

/**
 * Check string.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isString(value) {
    return typeof value === "string";
}

/**
 * Check function.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isFunction(value) {
    return typeof value === "function";
}

/**
 * Check plain object.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isObject(value) {
    return value !== null &&
        typeof value === "object" &&
        !Array.isArray(value);
}

/**
 * Check Blob.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isBlob(value) {
    return value instanceof Blob;
}

/**
 * Check File.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isFile(value) {
    return value instanceof File;
}

/**
 * Check image file.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isImageFile(value) {
    return (
        isFile(value) &&
        value.type.startsWith("image/")
    );
}

/**
 * Check HTMLImageElement.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isImageElement(value) {
    return value instanceof HTMLImageElement;
}

/**
 * Check HTMLCanvasElement.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isCanvas(value) {
    return value instanceof HTMLCanvasElement;
}

/**
 * Check null.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isNull(value) {
    return value === null;
}

/**
 * Check undefined.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isUndefined(value) {
    return value === undefined;
}

/* --------------------------------------------------------
 * Export Helpers
 * ------------------------------------------------------ */

/**
 * Default no-operation function.
 */
export function noop() {}
