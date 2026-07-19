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
 * @returns {NodeListOf<Element>}
 */
export function queryAll(selector, parent = document) {
    return parent.querySelectorAll(selector);
}

/**
 * Show an element.
 *
 * @param {HTMLElement} element
 */
export function show(element) {

    if (!element) return;

    element.classList.remove("hidden");
}

/**
 * Hide an element.
 *
 * @param {HTMLElement} element
 */
export function hide(element) {

    if (!element) return;

    element.classList.add("hidden");
}

/**
 * Toggle visibility.
 *
 * @param {HTMLElement} element
 */
export function toggle(element) {

    if (!element) return;

    element.classList.toggle("hidden");
}

/**
 * Add CSS class.
 *
 * @param {HTMLElement} element
 * @param {string} className
 */
export function addClass(element, className) {

    if (!element) return;

    element.classList.add(className);
}

/**
 * Remove CSS class.
 *
 * @param {HTMLElement} element
 * @param {string} className
 */
export function removeClass(element, className) {

    if (!element) return;

    element.classList.remove(className);
}

/**
 * Toggle CSS class.
 *
 * @param {HTMLElement} element
 * @param {string} className
 */
export function toggleClass(element, className) {

    if (!element) return;

    element.classList.toggle(className);
}

/**
 * Enable button.
 *
 * @param {HTMLButtonElement} button
 */
export function enableButton(button) {

    if (!button) return;

    button.disabled = false;
}

/**
 * Disable button.
 *
 * @param {HTMLButtonElement} button
 */
export function disableButton(button) {

    if (!button) return;

    button.disabled = true;
}

/**
 * Display field validation error.
 *
 * @param {HTMLElement} field
 * @param {string} message
 */
export function showFieldError(field, message) {

    if (!field) return;

    field.classList.add(
        "border-red-500",
        "focus:border-red-500",
        "focus:ring-red-500"
    );

    let error = field.parentElement.querySelector(".field-error");

    if (!error) {

        error = document.createElement("p");

        error.className =
            "field-error mt-1 text-sm text-red-500";

        field.parentElement.appendChild(error);
    }

    error.textContent = message;
}

/**
 * Remove field validation error.
 *
 * @param {HTMLElement} field
 */
export function clearFieldError(field) {

    if (!field) return;

    field.classList.remove(
        "border-red-500",
        "focus:border-red-500",
        "focus:ring-red-500"
    );

    const error =
        field.parentElement.querySelector(".field-error");

    if (error) {
        error.remove();
    }
}

/**
 * Remove all validation errors inside a form.
 *
 * @param {HTMLFormElement} form
 */
export function clearFormErrors(form) {

    if (!form) return;

    form.querySelectorAll(".field-error")
        .forEach(error => error.remove());

    form.querySelectorAll(
        ".border-red-500"
    ).forEach(field => {

        field.classList.remove(
            "border-red-500",
            "focus:border-red-500",
            "focus:ring-red-500"
        );

    });
}