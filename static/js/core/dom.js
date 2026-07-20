/*
===========================================================
File: static/js/core/dom.js
===========================================================

PURPOSE

Reusable DOM manipulation utilities.

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
 * Validation error classes.
 */
const ERROR_CLASSES = [
    "border-red-500",
    "focus:border-red-500",
    "focus:ring-red-500",
];

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
 * @param {string} selector
 * @param {ParentNode} parent
 * @returns {Element|null}
 */
export function query(selector, parent = document) {
    return parent.querySelector(selector);
}

/**
 * Query selector all.
 *
 * @param {string} selector
 * @param {ParentNode} parent
 * @returns {Element[]}
 */
export function queryAll(selector, parent = document) {
    return [...parent.querySelectorAll(selector)];
}

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
 * Toggle element visibility.
 *
 * @param {HTMLElement|null} element
 */
export function toggle(element) {

    if (!element) return;

    element.classList.toggle("hidden");
}

/**
 * Add CSS class.
 *
 * @param {HTMLElement|null} element
 * @param {...string} classNames
 */
export function addClass(element, ...classNames) {

    if (!element) return;

    element.classList.add(...classNames);
}

/**
 * Remove CSS class.
 *
 * @param {HTMLElement|null} element
 * @param {...string} classNames
 */
export function removeClass(element, ...classNames) {

    if (!element) return;

    element.classList.remove(...classNames);
}

/**
 * Toggle CSS class.
 *
 * @param {HTMLElement|null} element
 * @param {string} className
 */
export function toggleClass(element, className) {

    if (!element) return;

    element.classList.toggle(className);
}

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
}

/**
 * Get validation container.
 *
 * Uses `.form-field` wrapper if available.
 * Falls back to parentElement for backward compatibility.
 *
 * @param {HTMLElement} field
 * @returns {HTMLElement|null}
 */
function getFieldContainer(field) {

    return (
        field.closest(".form-field") ??
        field.parentElement
    );
}

/**
 * Display validation error.
 *
 * @param {HTMLElement|null} field
 * @param {string} message
 */
export function showFieldError(field, message) {

    if (!field) return;

    const container = getFieldContainer(field);

    if (!container) return;

    field.classList.add(...ERROR_CLASSES);

    let error =
        container.querySelector(".field-error");

    if (!error) {

        error = document.createElement("p");

        error.className =
            "field-error mt-1 text-sm text-red-500";

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

    if (!container) return;

    const error =
        container.querySelector(".field-error");

    error?.remove();
}

/**
 * Remove all validation errors.
 *
 * @param {HTMLFormElement|null} form
 */
export function clearFormErrors(form) {

    if (!form) return;

    form
        .querySelectorAll(".field-error")
        .forEach(error => error.remove());

    form
        .querySelectorAll("*")
        .forEach(element => {

            element.classList.remove(
                ...ERROR_CLASSES
            );

        });

}