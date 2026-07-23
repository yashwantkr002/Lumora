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
✓ Password Strength
✓ Password Match
✓ Client Validation
✓ Loading State
✓ Double Submit Prevention

===========================================================
*/

"use strict";

import { togglePassword, getPasswordStrength, passwordsMatch } from "./auth.js";

import {
  getElement,
  show,
  hide,
  on,
  ready,
  setText,
  clearFormErrors,
} from "../core/dom.js";

import {
  validateRequiredField,
  validateEmailField,
  validateUsernameField,
  validatePasswordField,
  validateConfirmPasswordField,
} from "../core/validation.js";

import { trim, setButtonLoading, resetButtonLoading } from "../core/utils.js";

ready(() => {
  const form = getElement("registerForm");

  if (!(form instanceof HTMLFormElement)) {
    return;
  }

  //--------------------------------------------------
  // Fields
  //--------------------------------------------------

  const firstNameField = getElement("firstName");
  const lastNameField = getElement("lastName");
  const usernameField = getElement("username");
  const emailField = getElement("email");

  const passwordField = getElement("password");
  const confirmPasswordField = getElement("confirmPassword");

  const registerButton = getElement("registerButton");

  //--------------------------------------------------
  // Password UI
  //--------------------------------------------------

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
    !(firstNameField instanceof HTMLInputElement) ||
    !(lastNameField instanceof HTMLInputElement) ||
    !(usernameField instanceof HTMLInputElement) ||
    !(emailField instanceof HTMLInputElement) ||
    !(passwordField instanceof HTMLInputElement) ||
    !(confirmPasswordField instanceof HTMLInputElement) ||
    !(registerButton instanceof HTMLButtonElement)
  ) {
    console.error("Register page initialization failed.");

    return;
  }

  let isSubmitting = false;

  //--------------------------------------------------
  // Auto Focus
  //--------------------------------------------------

  firstNameField.focus();

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

      setText(
        passwordMatchMessage,

        "✓ Passwords match",
      );
    } else {
      passwordMatchMessage.className = "mt-2 text-sm text-red-500";

      setText(
        passwordMatchMessage,

        "✗ Passwords do not match",
      );
    }
  }

  on(passwordField, "input", updatePasswordMatch);

  on(confirmPasswordField, "input", updatePasswordMatch);

  // -------------------------------------------------
  // PART 2 STARTS HERE
  // (Validation + Submit + Loading + PageShow)
  // -------------------------------------------------
  /* --------------------------------------------------
   * Validation
   * -------------------------------------------------- */

  function validateForm() {
    clearFormErrors(form);

    firstNameField.value = trim(firstNameField.value);
    lastNameField.value = trim(lastNameField.value);
    usernameField.value = trim(usernameField.value);
    emailField.value = trim(emailField.value);
    passwordField.value = trim(passwordField.value);
    confirmPasswordField.value = trim(confirmPasswordField.value);

    const firstNameValid = validateRequiredField(
      firstNameField,
      "First name is required.",
    );

    const lastNameValid = validateRequiredField(
      lastNameField,
      "Last name is required.",
    );

    const usernameValid = validateUsernameField(usernameField);

    const emailValid = validateEmailField(emailField);

    const passwordValid = validatePasswordField(passwordField);

    const confirmPasswordValid = validateConfirmPasswordField(
      passwordField,
      confirmPasswordField,
    );

    return (
      firstNameValid &&
      lastNameValid &&
      usernameValid &&
      emailValid &&
      passwordValid &&
      confirmPasswordValid
    );
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

    setButtonLoading(registerButton, "Creating Account...");
  });

  /* --------------------------------------------------
   * Reset Loading (Browser Back)
   * -------------------------------------------------- */

  on(window, "pageshow", () => {
    isSubmitting = false;

    resetButtonLoading(registerButton);
  });
});
