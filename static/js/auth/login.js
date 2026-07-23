/*
===========================================================
File: static/js/auth/login.js
===========================================================

PURPOSE

Handles login page interactions.

Features

✓ Client Validation
✓ Password Toggle
✓ Loading Button
✓ Double Submit Prevention
✓ Auto Focus
✓ Trim Inputs
✓ Validation UI
✓ Browser Back Recovery
✓ Production Ready

===========================================================
*/

"use strict";

import { togglePassword } from "./auth.js";

import {
    getElement,
    on,
    ready,
    clearFormErrors,
} from "../core/dom.js";

import {
    validateRequiredField,
} from "../core/validation.js";

import {
    trim,
    setButtonLoading,
    resetButtonLoading,
} from "../core/utils.js";

ready(() => {

    /* ----------------------------------------------------
     * Elements
     * -------------------------------------------------- */

    const form = getElement("loginForm");

    if (!(form instanceof HTMLFormElement)) {
        return;
    }

    const usernameInput = getElement("usernameOrEmail");
    const passwordInput = getElement("password");
    const submitButton = getElement("loginButton");
    const toggleButton = getElement("togglePassword");
    const toggleIcon = getElement("togglePasswordIcon");

    if (
        !(usernameInput instanceof HTMLInputElement) ||
        !(passwordInput instanceof HTMLInputElement) ||
        !(submitButton instanceof HTMLButtonElement)
    ) {
        return;
    }

    /* ----------------------------------------------------
     * State
     * -------------------------------------------------- */

    let isSubmitting = false;

    /* ----------------------------------------------------
     * Helpers
     * -------------------------------------------------- */

    function normalizeInputs() {

        usernameInput.value = trim(usernameInput.value);

        passwordInput.value = trim(passwordInput.value);

    }

    function validateForm() {

        clearFormErrors(form);

        normalizeInputs();

        const usernameValid = validateRequiredField(
            usernameInput,
            "Username or Email is required.",
        );

        const passwordValid = validateRequiredField(
            passwordInput,
            "Password is required.",
        );

        return usernameValid && passwordValid;

    }

    function beginSubmit() {

        isSubmitting = true;

        setButtonLoading(
            submitButton,
            "Signing In...",
        );

    }

    function endSubmit() {

        isSubmitting = false;

        resetButtonLoading(submitButton);

    }

    /* ----------------------------------------------------
     * Initial Focus
     * -------------------------------------------------- */

    usernameInput.focus();

    /* ----------------------------------------------------
     * Password Toggle
     * -------------------------------------------------- */

    if (toggleButton) {

        on(toggleButton, "click", () => {

            togglePassword(
                passwordInput,
                toggleIcon,
            );

        });

    }

    /* ----------------------------------------------------
     * Submit
     * -------------------------------------------------- */

    on(form, "submit", (event) => {

        if (isSubmitting) {

            event.preventDefault();

            return;

        }

        if (!validateForm()) {

            event.preventDefault();

            return;

        }

        beginSubmit();

        /*
         * Normal Django form submit.
         * Do not preventDefault().
         */

    });

    /* ----------------------------------------------------
     * Restore State (Back/Forward Cache)
     * -------------------------------------------------- */

    on(window, "pageshow", () => {

        endSubmit();

    });

});