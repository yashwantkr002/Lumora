/*
===========================================================
File: static/js/auth/change-password.js
===========================================================

PURPOSE

Handles change password page interactions.

Features

✓ Password Toggle
✓ Confirm Password Toggle
✓ Trim Inputs
✓ Client Validation
✓ Loading Button
✓ Password Strength
✓ Password Match

===========================================================
*/

"use strict";

import {
  togglePassword,
  setLoading,
  resetLoading,
  trimInputs,
} from "./auth.js";

import {
  getElement,
  show,
  hide,
  showFieldError,
  clearFormErrors,
} from "../core/dom.js";

import {
  validateRequired,
  validatePassword,
  validateConfirmPassword,
} from "../core/validation.js";

document.addEventListener("DOMContentLoaded", initializeChangePassword);

/**
 * Initialize change password page.
 */
function initializeChangePassword() {
  const form = getElement("changePasswordForm");

  if (!form) {
    return;
  }

  const currentPasswordField = getElement("id_old_password");
  const newPasswordField = getElement("id_new_password1");
  const confirmPasswordField = getElement("id_new_password2");

  const toggleCurrentPasswordButton = getElement("toggleCurrentPassword");
  const togglePasswordButton = getElement("togglePassword");
  const toggleConfirmPasswordButton = getElement("toggleConfirmPassword");

  const strengthContainer = getElement("passwordStrength");
  const strengthBar = getElement("strengthBar");
  const strengthText = getElement("strengthText");
  const passwordMatchMessage = getElement("passwordMatchMessage");
  const changePasswordButton = getElement("changePasswordButton");

  currentPasswordField?.focus();

  toggleCurrentPasswordButton?.addEventListener("click", () => {
    togglePassword(currentPasswordField, toggleCurrentPasswordButton);
  });

  togglePasswordButton?.addEventListener("click", () => {
    togglePassword(newPasswordField, togglePasswordButton);
  });

  toggleConfirmPasswordButton?.addEventListener("click", () => {
    togglePassword(confirmPasswordField, toggleConfirmPasswordButton);
  });

  form.addEventListener("submit", (event) => {
    clearFormErrors(form);

    trimInputs(form);

    let valid = true;

    if (!validateRequired(currentPasswordField?.value)) {
      showFieldError(currentPasswordField, "Current password is required.");
      valid = false;
    }

    if (!validateRequired(newPasswordField?.value)) {
      showFieldError(newPasswordField, "New password is required.");
      valid = false;
    } else if (!validatePassword(newPasswordField.value)) {
      showFieldError(
        newPasswordField,
        "Password must be at least 8 characters and include uppercase, lowercase, number, and special character."
      );
      valid = false;
    }

    if (!validateRequired(confirmPasswordField?.value)) {
      showFieldError(confirmPasswordField, "Please confirm your new password.");
      valid = false;
    } else if (
      !validateConfirmPassword(newPasswordField?.value, confirmPasswordField?.value)
    ) {
      showFieldError(confirmPasswordField, "Passwords do not match.");
      valid = false;
    }

    if (!valid) {
      event.preventDefault();
      return;
    }

    setLoading(changePasswordButton, "Updating Password...");
  });

  initializePasswordStrength(
    newPasswordField,
    strengthContainer,
    strengthBar,
    strengthText
  );

  initializePasswordMatch(
    newPasswordField,
    confirmPasswordField,
    passwordMatchMessage
  );

  window.addEventListener("pageshow", () => {
    resetLoading(changePasswordButton);
  });
}

/**
 * Live password strength meter.
 */
function initializePasswordStrength(passwordField, container, bar, text) {
  if (!passwordField) return;

  passwordField.addEventListener("input", () => {
    const password = passwordField.value;

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

    updateStrengthUI(score, bar, text);
  });
}

/**
 * Update strength UI.
 */
function updateStrengthUI(score, bar, text) {
  bar.className = "h-full rounded-full transition-all duration-300";

  if (score <= 2) {
    bar.classList.add("w-1/3", "bg-red-500");
    text.textContent = "Weak Password";
    return;
  }

  if (score <= 4) {
    bar.classList.add("w-2/3", "bg-yellow-500");
    text.textContent = "Medium Password";
    return;
  }

  bar.classList.add("w-full", "bg-green-500");
  text.textContent = "Strong Password";
}

/**
 * Live password match feedback.
 */
function initializePasswordMatch(passwordField, confirmPasswordField, message) {
  if (!confirmPasswordField) return;

  function update() {
    if (!confirmPasswordField.value) {
      message.textContent = "";
      return;
    }

    const match = validateConfirmPassword(passwordField?.value, confirmPasswordField.value);

    if (match) {
      message.textContent = "✓ Passwords match";
      message.className = "mt-2 text-sm text-green-600";
    } else {
      message.textContent = "✗ Passwords do not match";
      message.className = "mt-2 text-sm text-red-500";
    }
  }

  passwordField?.addEventListener("input", update);
  confirmPasswordField.addEventListener("input", update);
}
