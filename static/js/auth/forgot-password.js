/*
===========================================================
File: static/js/auth/forgot-password.js
===========================================================

PURPOSE

Handles forgot password page interactions.

===========================================================
*/

"use strict";

import {
    trimInputs,
    setLoading,
    resetLoading,
} from "./auth.js";

import {
    getElement,
    showFieldError,
    clearFormErrors,
} from "../core/dom.js";

import {
    validateRequired,
    validateEmail,
} from "../core/validation.js";

document.addEventListener(
    "DOMContentLoaded",
    initializeForgotPassword,
);

function initializeForgotPassword() {

    const form =
        getElement("forgotPasswordForm");

    if (!form) return;

    const email =
        getElement("email");

    const button =
        getElement("forgotPasswordButton");

    email?.focus();

    form.addEventListener(
        "submit",
        event => {

            clearFormErrors(form);

            trimInputs(form);

            let valid = true;

            if (!validateRequired(email.value)) {

                showFieldError(
                    email,
                    "Email is required."
                );

                valid = false;

            } else if (!validateEmail(email.value)) {

                showFieldError(
                    email,
                    "Enter a valid email address."
                );

                valid = false;

            }

            if (!valid) {

                event.preventDefault();

                return;

            }

            setLoading(
                button,
                "Sending..."
            );

        }
    );

    window.addEventListener(
        "pageshow",
        () => resetLoading(button)
    );

}