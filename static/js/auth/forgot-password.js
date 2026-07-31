/*
===========================================================
File: static/js/auth/forgot-password.js
===========================================================

PURPOSE

Handles forgot password page interactions.

Features

✓ Auto Focus
✓ Client Validation
✓ Trim Inputs
✓ Loading State
✓ Double Submit Prevention

===========================================================
*/

"use strict";

import { ready, on, getElement, clearFormErrors } from "../core/dom.js";

import { validateEmailField } from "../core/validation.js";

import { trim, setButtonLoading, resetButtonLoading } from "../core/utils.js";

ready(() => {
  //--------------------------------------------------
  // Elements
  //--------------------------------------------------

  const form = getElement("forgotPasswordForm");

  if (!(form instanceof HTMLFormElement)) {
    return;
  }

  const emailField = getElement("email");

  const submitButton = getElement("forgotPasswordButton");

  if (
    !(emailField instanceof HTMLInputElement) ||
    !(submitButton instanceof HTMLButtonElement)
  ) {
    console.error("Forgot Password page initialization failed.");

    return;
  }

  let isSubmitting = false;

  //--------------------------------------------------
  // Auto Focus
  //--------------------------------------------------

  emailField.focus();

  //--------------------------------------------------
  // Validation
  //--------------------------------------------------

  function validateForm() {
    clearFormErrors(form);

    emailField.value = trim(emailField.value);

    return validateEmailField(emailField);
  }

  //--------------------------------------------------
  // Submit
  //--------------------------------------------------

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

    setButtonLoading(submitButton, "Sending...");
  });

  //--------------------------------------------------
  // Browser Back Button
  //--------------------------------------------------

  on(window, "pageshow", () => {
    isSubmitting = false;

    resetButtonLoading(submitButton);
  });
});
