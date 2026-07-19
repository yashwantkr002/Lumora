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

/**
 * Debounce function.
 *
 * @param {Function} callback
 * @param {number} delay
 * @returns {Function}
 */
export function debounce(callback, delay = 300) {

    let timeoutId;

    return (...args) => {

        clearTimeout(timeoutId);

        timeoutId = setTimeout(() => {
            callback(...args);
        }, delay);

    };

}

/**
 * Throttle function.
 *
 * @param {Function} callback
 * @param {number} delay
 * @returns {Function}
 */
export function throttle(callback, delay = 300) {

    let waiting = false;

    return (...args) => {

        if (waiting) return;

        callback(...args);

        waiting = true;

        setTimeout(() => {
            waiting = false;
        }, delay);

    };

}

/**
 * Sleep helper.
 *
 * @param {number} milliseconds
 * @returns {Promise<void>}
 */
export function sleep(milliseconds) {

    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });

}

/**
 * Capitalize first letter.
 *
 * @param {string} value
 * @returns {string}
 */
export function capitalize(value) {

    if (!value) return "";

    return value.charAt(0).toUpperCase() + value.slice(1);

}

/**
 * Generate UUID.
 *
 * @returns {string}
 */
export function generateUUID() {

    return crypto.randomUUID();

}

/**
 * Copy text to clipboard.
 *
 * @param {string} text
 * @returns {Promise<void>}
 */
export async function copyToClipboard(text) {

    await navigator.clipboard.writeText(text);

}

/**
 * Check mobile device.
 *
 * @returns {boolean}
 */
export function isMobile() {

    return window.innerWidth < 768;

}

/**
 * Format date.
 *
 * @param {string|Date} date
 * @param {string} locale
 * @returns {string}
 */
export function formatDate(
    date,
    locale = "en-IN",
) {

    return new Intl.DateTimeFormat(
        locale,
        {
            dateStyle: "medium",
            timeStyle: "short",
        },
    ).format(new Date(date));

}

/**
 * Trim string safely.
 *
 * @param {string} value
 * @returns {string}
 */
export function trim(value) {

    return typeof value === "string"
        ? value.trim()
        : "";

}

/**
 * Check if value is empty.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isEmpty(value) {

    if (value == null) {
        return true;
    }

    if (typeof value === "string") {
        return value.trim() === "";
    }

    if (Array.isArray(value)) {
        return value.length === 0;
    }

    return false;

}