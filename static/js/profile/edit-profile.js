/*
===========================================================
File: static/js/profile/edit-profile.js
===========================================================

PURPOSE

Handles edit profile page interactions.

Features

✓ Form Validation
✓ Field Error Handling
✓ Avatar Upload Preview
✓ Save Button Loading
✓ Form Reset
✓ Client-side Validation

===========================================================
*/

"use strict";

import {
  getElement,
  ready,
  on,
  clearFormErrors,
} from "../core/dom.js";

import {
  validateRequiredField,
  validateEmailField,
  validateUsernameField,
} from "../core/validation.js";

import {
  trim,
  setButtonLoading,
  resetButtonLoading,
} from "../core/utils.js";

// Import specialized profile modules
import "./avatar.js";
import "./cover.js";
import "./bio-counter.js";
import { cropImage, scaleImageOnCanvas, exportCanvasAsBlob } from "./cropper.js";

ready(() => {
  /* --------------------------------------------------
   * Elements
   * -------------------------------------------------- */

  const form = getElement("editProfileForm");

  if (!(form instanceof HTMLFormElement)) {
    return;
  }

  const firstNameField = getElement("firstName");
  const lastNameField = getElement("lastName");
  const usernameField = getElement("username");
  const emailField = getElement("email");
  const bioField = getElement("bio");
  const saveButton =
    getElement("saveProfileButton") || getElement("saveButton");

  if (
    !(firstNameField instanceof HTMLInputElement) ||
    !(lastNameField instanceof HTMLInputElement) ||
    !(usernameField instanceof HTMLInputElement) ||
    !(emailField instanceof HTMLInputElement) ||
    !(bioField instanceof HTMLTextAreaElement) ||
    !(saveButton instanceof HTMLButtonElement)
  ) {
    return;
  }

  let isSubmitting = false;

  /* --------------------------------------------------
   * Form Validation
   * -------------------------------------------------- */

  function validateForm() {
    clearFormErrors(form);

    firstNameField.value = trim(firstNameField.value);
    lastNameField.value = trim(lastNameField.value);
    usernameField.value = trim(usernameField.value);
    emailField.value = trim(emailField.value);
    bioField.value = trim(bioField.value);

    const firstNameValid = validateRequiredField(
      firstNameField,
      "First name is required."
    );

    const lastNameValid = validateRequiredField(
      lastNameField,
      "Last name is required."
    );

    const usernameValid = validateUsernameField(usernameField);

    const emailValid = validateEmailField(emailField);

    return (
      firstNameValid &&
      lastNameValid &&
      usernameValid &&
      emailValid
    );
  }

  /* --------------------------------------------------
   * Submit Handler
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
    setButtonLoading(saveButton, "Saving...");

    /*
     * Normal Django form submit.
     * Do not preventDefault().
     */
  });

  /* --------------------------------------------------
   * Restore State (Back/Forward Cache)
   * -------------------------------------------------- */

  on(window, "pageshow", () => {
    isSubmitting = false;
    resetButtonLoading(saveButton);
  });
});