/*
===========================================================
File: static/js/auth/auth.js
===========================================================

PURPOSE

Reusable utilities for authentication pages.

Used By

- login.js
- register.js
- forgot-password.js
- reset-password.js
- change-password.js

===========================================================
*/

"use strict";

/**
 * Toggle password visibility.
 *
 * @param {HTMLInputElement} input
 * @param {HTMLElement|null} icon
 */
export function togglePassword(input, icon = null) {
    console.log("password toggle function called");
    if (!input) return;

    const isPassword = input.type === "password";

    input.type = isPassword ? "text" : "password";

    if (icon) {
        icon.classList.toggle("fa-eye");
        icon.classList.toggle("fa-eye-slash");
    }
}

/**
 * Disable submit button and show loading text.
 *
 * @param {HTMLButtonElement} button
 * @param {string} loadingText
 */
export function setLoading(button, loadingText = "Please wait...") {

    if (!button) return;

    button.disabled = true;

    button.dataset.originalText = button.innerHTML;

    button.innerHTML = `
        <span class="inline-flex items-center gap-2">
            <span class="animate-spin">⏳</span>
            ${loadingText}
        </span>
    `;
}

/**
 * Restore button.
 *
 * @param {HTMLButtonElement} button
 */
export function resetLoading(button) {

    if (!button) return;

    button.disabled = false;

    if (button.dataset.originalText) {
        button.innerHTML = button.dataset.originalText;
    }
}

/**
 * Trim all text inputs inside a form.
 *
 * @param {HTMLFormElement} form
 */
export function trimInputs(form) {

    if (!form) return;

    form.querySelectorAll("input[type='text'], input[type='email']")
        .forEach(input => {
            input.value = input.value.trim();
        });
}

/**
 * Check required fields.
 *
 * @param {HTMLFormElement} form
 * @returns {boolean}
 */
export function validateRequired(form) {

    let valid = true;

    form.querySelectorAll("[required]").forEach(field => {

        if (field.value.trim() === "") {

            field.classList.add(
                "border-red-500",
                "focus:border-red-500"
            );

            valid = false;

        } else {

            field.classList.remove(
                "border-red-500",
                "focus:border-red-500"
            );
        }

    });

    return valid;
}