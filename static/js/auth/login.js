/*
===========================================================
File: static/js/auth/login.js
===========================================================

PURPOSE

Handles login page interactions.

Features

✓ Client Validation
✓ Loading Button
✓ Password Toggle
✓ Double Submit Prevention
✓ Auto Focus
✓ Trim Inputs

===========================================================
*/

"use strict";

import {
    togglePassword,
    setLoading,
    resetLoading,
    trimInputs,
    validateRequired,
} from "./auth.js";

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("loginForm");

    if (!form) return;

    const usernameInput = document.getElementById("usernameOrEmail");

    const passwordInput = document.getElementById("password");

    const submitButton = document.getElementById("loginButton");

    const toggleButton = document.getElementById("togglePassword");

    const toggleIcon = document.getElementById("togglePasswordIcon");

    //------------------------------------------------------
    // Autofocus
    //------------------------------------------------------

    usernameInput?.focus();

    //------------------------------------------------------
    // Password Toggle
    //------------------------------------------------------

    toggleButton?.addEventListener("click", () => {

        togglePassword(
            passwordInput,
            toggleIcon
        );

    });

    //------------------------------------------------------
    // Submit
    //------------------------------------------------------

    form.addEventListener("submit", (event) => {

        trimInputs(form);

        if (!validateRequired(form)) {

            event.preventDefault();

            return;

        }

        setLoading(
            submitButton,
            "Signing In..."
        );

    });

    //------------------------------------------------------
    // Browser Back Button
    //------------------------------------------------------

    window.addEventListener("pageshow", () => {

        resetLoading(submitButton);

    });

});