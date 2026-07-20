/*
===========================================================
File: static/js/auth/reset-password.js
===========================================================

PURPOSE

Handles reset password page interactions.

Features

✓ Auto Focus
✓ Password Toggle
✓ Confirm Password Toggle
✓ Password Strength Meter
✓ Live Password Match
✓ Client Validation
✓ Trim Inputs
✓ Loading Button
✓ Double Submit Prevention
✓ Browser Back Restore

===========================================================
*/

"use strict";

import {
    togglePassword,
    trimInputs,
    setLoading,
    resetLoading,
} from "./auth.js";

import {
    getElement,
    show,
    hide,
    showFieldError,
    clearFormErrors,
} from "../core/dom.js";

import {
    validatePassword,
    validateConfirmPassword,
} from "../core/validation.js";

document.addEventListener(
    "DOMContentLoaded",
    initializeResetPassword,
);

/**
 * Initialize reset password page.
 */
function initializeResetPassword() {

    const form = getElement("resetPasswordForm");

    if (!form) return;

    const passwordField = getElement("password");

    const confirmPasswordField = getElement("confirmPassword");

    const togglePasswordButton = getElement("togglePassword");

    const toggleConfirmPasswordButton =
        getElement("toggleConfirmPassword");

    const strengthContainer =
        getElement("passwordStrength");

    const strengthBar =
        getElement("strengthBar");

    const strengthText =
        getElement("strengthText");

    const passwordMatchMessage =
        getElement("passwordMatchMessage");

    const resetButton =
        getElement("resetPasswordButton");

    //----------------------------------------------------
    // Auto Focus
    //----------------------------------------------------

    passwordField?.focus();

    //----------------------------------------------------
    // Password Toggle
    //----------------------------------------------------

    togglePasswordButton?.addEventListener(
        "click",
        () => togglePassword(
            passwordField,
            togglePasswordButton,
        ),
    );

    //----------------------------------------------------
    // Confirm Password Toggle
    //----------------------------------------------------

    toggleConfirmPasswordButton?.addEventListener(
        "click",
        () => togglePassword(
            confirmPasswordField,
            toggleConfirmPasswordButton,
        ),
    );

    //----------------------------------------------------
    // Submit
    //----------------------------------------------------

    form.addEventListener(
        "submit",
        event => {

            clearFormErrors(form);

            trimInputs(form);

            let valid = true;

            if (!validatePassword(passwordField.value)) {

                showFieldError(
                    passwordField,
                    "Password does not meet the requirements.",
                );

                valid = false;

            }

            if (
                !validateConfirmPassword(
                    passwordField.value,
                    confirmPasswordField.value,
                )
            ) {

                showFieldError(
                    confirmPasswordField,
                    "Passwords do not match.",
                );

                valid = false;

            }

            if (!valid) {

                event.preventDefault();

                return;

            }

            setLoading(
                resetButton,
                "Resetting Password...",
            );

        },
    );

    //----------------------------------------------------
    // Password Strength
    //----------------------------------------------------

    initializePasswordStrength(
        passwordField,
        strengthContainer,
        strengthBar,
        strengthText,
    );

    //----------------------------------------------------
    // Password Match
    //----------------------------------------------------

    initializePasswordMatch(
        passwordField,
        confirmPasswordField,
        passwordMatchMessage,
    );

    //----------------------------------------------------
    // Browser Back Restore
    //----------------------------------------------------

    window.addEventListener(
        "pageshow",
        () => resetLoading(resetButton),
    );

}

/**
 * Live password strength.
 */
function initializePasswordStrength(
    passwordField,
    container,
    bar,
    text,
) {

    if (!passwordField) return;

    passwordField.addEventListener(
        "input",
        () => {

            const password =
                passwordField.value;

            if (!password) {

                hide(container);

                return;

            }

            show(container);

            let score = 0;

            if (password.length >= 8) score++;

            if (/[a-z]/.test(password)) score++;

            if (/[A-Z]/.test(password)) score++;

            if (/\d/.test(password)) score++;

            if (/[^A-Za-z0-9]/.test(password)) score++;

            updateStrengthUI(
                score,
                bar,
                text,
            );

        },
    );

}

/**
 * Update strength meter.
 */
function updateStrengthUI(
    score,
    bar,
    text,
) {

    bar.className =
        "h-full rounded-full transition-all duration-300";

    if (score <= 2) {

        bar.classList.add(
            "w-1/3",
            "bg-red-500",
        );

        text.textContent =
            "Weak Password";

        return;

    }

    if (score <= 4) {

        bar.classList.add(
            "w-2/3",
            "bg-yellow-500",
        );

        text.textContent =
            "Medium Password";

        return;

    }

    bar.classList.add(
        "w-full",
        "bg-green-500",
    );

    text.textContent =
        "Strong Password";

}

/**
 * Live password match.
 */
function initializePasswordMatch(
    passwordField,
    confirmPasswordField,
    message,
) {

    if (!confirmPasswordField) return;

    function update() {

        if (!confirmPasswordField.value) {

            message.textContent = "";

            return;

        }

        const match =
            validateConfirmPassword(
                passwordField.value,
                confirmPasswordField.value,
            );

        if (match) {

            message.textContent =
                "✓ Passwords match";

            message.className =
                "mt-2 text-sm text-green-600";

        } else {

            message.textContent =
                "✗ Passwords do not match";

            message.className =
                "mt-2 text-sm text-red-500";

        }

    }

    passwordField.addEventListener(
        "input",
        update,
    );

    confirmPasswordField.addEventListener(
        "input",
        update,
    );

}