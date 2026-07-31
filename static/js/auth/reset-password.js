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
✓ Loading Button
✓ Double Submit Prevention
✓ Browser Back Restore

===========================================================
*/

"use strict";

import { togglePassword, getPasswordStrength, passwordsMatch } from "./auth.js";

import {
  ready,
  on,
  getElement,
  show,
  hide,
  setText,
  clearFormErrors,
} from "../core/dom.js";

import {
  validatePasswordField,
  validateConfirmPasswordField,
} from "../core/validation.js";

import { trim, setButtonLoading, resetButtonLoading } from "../core/utils.js";

ready(() => {
  //--------------------------------------------------
  // Elements
  //--------------------------------------------------

  const form = getElement("resetPasswordForm");

  if (!(form instanceof HTMLFormElement)) {
    return;
  }

  const passwordField = getElement("password");

  const confirmPasswordField = getElement("confirmPassword");

  const resetButton = getElement("resetPasswordButton");

  const togglePasswordButton = getElement("togglePassword");

  const toggleConfirmPasswordButton = getElement("toggleConfirmPassword");

  const strengthContainer = getElement("passwordStrength");

  const strengthBar = getElement("strengthBar");

  const strengthText = getElement("strengthText");

  const passwordMatchMessage = getElement("passwordMatchMessage");

  //--------------------------------------------------
  // Safety Check
  //--------------------------------------------------

  if (
    !(passwordField instanceof HTMLInputElement) ||
    !(confirmPasswordField instanceof HTMLInputElement) ||
    !(resetButton instanceof HTMLButtonElement)
  ) {
    console.error("Reset Password page initialization failed.");

    return;
  }

  let isSubmitting = false;

  //--------------------------------------------------
  // Auto Focus
  //--------------------------------------------------

  passwordField.focus();

  //--------------------------------------------------
  // Password Toggle
  //--------------------------------------------------

  if (togglePasswordButton) {
    on(togglePasswordButton, "click", () => {
      togglePassword(passwordField, togglePasswordButton);
    });
  }

  //--------------------------------------------------
  // Confirm Password Toggle
  //--------------------------------------------------

  if (toggleConfirmPasswordButton) {
    on(toggleConfirmPasswordButton, "click", () => {
      togglePassword(confirmPasswordField, toggleConfirmPasswordButton);
    });
  }

  //--------------------------------------------------
  // Live Password Strength
  //--------------------------------------------------

  on(passwordField, "input", () => {
    const password = trim(passwordField.value);

    if (!password) {
      hide(strengthContainer);

      return;
    }

    show(strengthContainer);

    const strength = getPasswordStrength(password);

    strengthBar.className = `h-full rounded-full transition-all duration-300 ${strength.color}`;

    switch (strength.score) {
      case 0:
      case 1:
        strengthBar.style.width = "20%";
        break;

      case 2:
        strengthBar.style.width = "40%";
        break;

      case 3:
        strengthBar.style.width = "60%";
        break;

      case 4:
        strengthBar.style.width = "80%";
        break;

      default:
        strengthBar.style.width = "100%";
    }

    setText(strengthText, strength.label);
  });

  //--------------------------------------------------
  // Live Password Match
  //--------------------------------------------------

  function updatePasswordMatch() {
    if (!confirmPasswordField.value) {
      setText(passwordMatchMessage, "");

      return;
    }

    const matched = passwordsMatch(
      passwordField.value,
      confirmPasswordField.value,
    );

    if (matched) {
      passwordMatchMessage.className = "mt-2 text-sm text-green-600";

      setText(passwordMatchMessage, "✓ Passwords match");
    } else {
      passwordMatchMessage.className = "mt-2 text-sm text-red-500";

      setText(passwordMatchMessage, "✗ Passwords do not match");
    }
  }

  on(passwordField, "input", updatePasswordMatch);

  on(confirmPasswordField, "input", updatePasswordMatch);

  // --------------------------------------------------
  // PART 2 STARTS HERE
  // (Validation + Submit + Browser Restore)
  // --------------------------------------------------
  /* --------------------------------------------------
   * Validation
   * -------------------------------------------------- */

  function validateForm() {
    clearFormErrors(form);

    passwordField.value = trim(passwordField.value);

    confirmPasswordField.value = trim(confirmPasswordField.value);

    const passwordValid = validatePasswordField(passwordField);

    const confirmPasswordValid = validateConfirmPasswordField(
      passwordField,
      confirmPasswordField,
    );

    return passwordValid && confirmPasswordValid;
  }

  /* --------------------------------------------------
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

    isSubmitting = true;

    setButtonLoading(resetButton, "Resetting Password...");
  });

  /* --------------------------------------------------
   * Browser Back Restore
   * -------------------------------------------------- */

  on(window, "pageshow", () => {
    isSubmitting = false;

    resetButtonLoading(resetButton);
  });
});
