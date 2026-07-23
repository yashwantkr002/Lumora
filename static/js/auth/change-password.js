/*
===========================================================
File: static/js/auth/change-password.js
===========================================================

PURPOSE

Handles change password page interactions.

Features

✓ Password Toggle
✓ Confirm Password Toggle
✓ Client Validation
✓ Password Strength
✓ Password Match
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
  validateRequiredField,
  validatePasswordField,
  validateConfirmPasswordField,
} from "../core/validation.js";

import { trim, setButtonLoading, resetButtonLoading } from "../core/utils.js";

ready(() => {
  //--------------------------------------------------
  // Elements
  //--------------------------------------------------

  const form = getElement("changePasswordForm");

  if (!(form instanceof HTMLFormElement)) {
    return;
  }

  const currentPasswordField = getElement("id_old_password");

  const newPasswordField = getElement("id_new_password1");

  const confirmPasswordField = getElement("id_new_password2");

  const changePasswordButton = getElement("changePasswordButton");

  const toggleCurrentPasswordButton = getElement("toggleCurrentPassword");

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
    !(currentPasswordField instanceof HTMLInputElement) ||
    !(newPasswordField instanceof HTMLInputElement) ||
    !(confirmPasswordField instanceof HTMLInputElement) ||
    !(changePasswordButton instanceof HTMLButtonElement)
  ) {
    console.error("Change Password page initialization failed.");

    return;
  }

  let isSubmitting = false;

  //--------------------------------------------------
  // Auto Focus
  //--------------------------------------------------

  currentPasswordField.focus();

  //--------------------------------------------------
  // Current Password Toggle
  //--------------------------------------------------

  if (toggleCurrentPasswordButton) {
    on(toggleCurrentPasswordButton, "click", () => {
      togglePassword(currentPasswordField, toggleCurrentPasswordButton);
    });
  }

  //--------------------------------------------------
  // New Password Toggle
  //--------------------------------------------------

  if (togglePasswordButton) {
    on(togglePasswordButton, "click", () => {
      togglePassword(newPasswordField, togglePasswordButton);
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

  on(newPasswordField, "input", () => {
    const password = trim(newPasswordField.value);

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
      newPasswordField.value,
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

  on(newPasswordField, "input", updatePasswordMatch);

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

    currentPasswordField.value = trim(currentPasswordField.value);

    newPasswordField.value = trim(newPasswordField.value);

    confirmPasswordField.value = trim(confirmPasswordField.value);

    const currentPasswordValid = validateRequiredField(
      currentPasswordField,
      "Current password is required.",
    );

    const newPasswordValid = validatePasswordField(newPasswordField);

    const confirmPasswordValid = validateConfirmPasswordField(
      newPasswordField,
      confirmPasswordField,
    );

    return currentPasswordValid && newPasswordValid && confirmPasswordValid;
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

    setButtonLoading(changePasswordButton, "Updating Password...");
  });

  /* --------------------------------------------------
   * Browser Back Restore
   * -------------------------------------------------- */

  on(window, "pageshow", () => {
    isSubmitting = false;

    resetButtonLoading(changePasswordButton);
  });
});
