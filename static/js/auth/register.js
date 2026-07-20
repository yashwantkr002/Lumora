/*
===========================================================
File: static/js/auth/register.js
===========================================================

PURPOSE

Handles register page interactions.

Features

✓ Auto Focus
✓ Password Toggle
✓ Confirm Password Toggle
✓ Trim Inputs

Remaining Features

- Password Strength
- Password Match
- Validation
- Loading State
- Double Submit Prevention

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
  validateRequired,
  validatePassword,
  validateConfirmPassword,
} from "../core/validation.js";
document.addEventListener("DOMContentLoaded", initializeRegister);

/**
 * Initialize register page.
 */
function initializeRegister() {
  const form = getElement("registerForm");

  if (!form) {
    return;
  }

  const firstNameField = getElement("firstName");

  const passwordField = getElement("password");

  const confirmPasswordField = getElement("confirmPassword");

  const togglePasswordButton = getElement("togglePassword");

  const toggleConfirmPasswordButton = getElement("toggleConfirmPassword");

  const strengthContainer = getElement("passwordStrength");

  const strengthBar = getElement("strengthBar");

  const strengthText = getElement("strengthText");

  const passwordMatchMessage = getElement("passwordMatchMessage");

  const registerButton = getElement("registerButton");

  //----------------------------------------------------
  // Auto Focus
  //----------------------------------------------------

  firstNameField?.focus();

  //----------------------------------------------------
  // Trim Inputs
  //----------------------------------------------------


  //----------------------------------------------------
  // Password Toggle
  //----------------------------------------------------

  togglePasswordButton?.addEventListener("click", () => {
    togglePassword(passwordField, togglePasswordButton);
  });

  //----------------------------------------------------
  // Confirm Password Toggle
  //----------------------------------------------------

  toggleConfirmPasswordButton?.addEventListener("click", () => {
    togglePassword(confirmPasswordField, toggleConfirmPasswordButton);
  });

  //----------------------------------------------------
  // Submit
  //----------------------------------------------------

  form.addEventListener("submit", (event) => {
    clearFormErrors(form);

    trimInputs(form);

    let valid = true;

    const firstName = getElement("firstName");
    const lastName = getElement("lastName");
    const username = getElement("username");
    const email = getElement("email");

    if (!validateRequired(firstName.value)) {
      showFieldError(firstName, "First name is required.");
      valid = false;
    }

    if (!validateRequired(lastName.value)) {
      showFieldError(lastName, "Last name is required.");
      valid = false;
    }

    if (!validateRequired(username.value)) {
      showFieldError(username, "Username is required.");
      valid = false;
    }

    if (!validateRequired(email.value)) {
      showFieldError(email, "Email is required.");
      valid = false;
    }

    if (!validatePassword(passwordField.value)) {
      showFieldError(passwordField, "Password does not meet the requirements.");

      valid = false;
    }

    if (
      !validateConfirmPassword(passwordField.value, confirmPasswordField.value)
    ) {
      showFieldError(confirmPasswordField, "Passwords do not match.");

      valid = false;
    }

    if (!valid) {
      event.preventDefault();

      return;
    }

    //------------------------------------------------
    // Loading State
    //------------------------------------------------

    setLoading(registerButton, "Creating Account...");
  });

  initializePasswordStrength(
    passwordField,
    strengthContainer,
    strengthBar,
    strengthText,
  );

  initializePasswordMatch(
    passwordField,
    confirmPasswordField,
    passwordMatchMessage,
  );

  window.addEventListener("pageshow", () => {
    resetLoading(registerButton);
  });
}

/**
 * Live password strength.
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
 * Update strength meter.
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
 * Live password matching.
 */
function initializePasswordMatch(passwordField, confirmPasswordField, message) {
  if (!confirmPasswordField) return;

  function update() {
    if (!confirmPasswordField.value) {
      message.textContent = "";

      return;
    }

    const match = validateConfirmPassword(
      passwordField.value,
      confirmPasswordField.value,
    );

    if (match) {
      message.textContent = "✓ Passwords match";

      message.className = "mt-2 text-sm text-green-600";
    } else {
      message.textContent = "✗ Passwords do not match";

      message.className = "mt-2 text-sm text-red-500";
    }
  }

  passwordField.addEventListener("input", update);

  confirmPasswordField.addEventListener("input", update);
}
