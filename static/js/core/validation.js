/*
===========================================================
File: static/js/core/validation.js
===========================================================

PURPOSE

Reusable validation utilities.

Used By

- Authentication
- Profile
- Posts
- Stories
- Comments
- Chat
- Notifications

===========================================================
*/

"use strict";

import { showFieldError, clearFieldError } from "./dom.js";

/* --------------------------------------------------------
 * Internal Helpers
 * ------------------------------------------------------ */

/**
 * Normalize a value.
 *
 * @param {*} value
 * @returns {string}
 */
function normalize(value) {
  return String(value ?? "").trim();
}

/**
 * Get field value.
 *
 * @param {HTMLInputElement|HTMLTextAreaElement|HTMLSelectElement|null} field
 * @returns {string}
 */
function getValue(field) {
  return normalize(field?.value);
}

/**
 * Set validation state.
 *
 * @param {HTMLElement} field
 * @param {boolean} valid
 * @param {string} message
 * @returns {boolean}
 */
function setValidationState(field, valid, message) {
  if (valid) {
    clearFieldError(field);

    return true;
  }

  showFieldError(field, message);

  return false;
}

/* --------------------------------------------------------
 * Pure Validators
 * ------------------------------------------------------ */

/**
 * Check empty value.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isEmpty(value) {
  return normalize(value) === "";
}

/**
 * Required validator.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function validateRequired(value) {
  return !isEmpty(value);
}

/**
 * Email validator.
 *
 * @param {*} email
 * @returns {boolean}
 */
export function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  return regex.test(normalize(email));
}

/**
 * Username validator.
 *
 * Rules:
 * - 3–30 chars
 * - Letters
 * - Numbers
 * - Underscore
 *
 * @param {*} username
 * @returns {boolean}
 */
export function validateUsername(username) {
  return /^[a-zA-Z0-9_]{3,30}$/.test(normalize(username));
}

/**
 * Password validator.
 *
 * @param {*} password
 * @returns {boolean}
 */
export function validatePassword(password) {
  return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&^#()_+\-=[\]{};':"\\|,.<>/?]).{8,}$/.test(
    String(password ?? ""),
  );
}

/**
 * Confirm password validator.
 *
 * @param {*} password
 * @param {*} confirmPassword
 * @returns {boolean}
 */
export function validateConfirmPassword(password, confirmPassword) {
  return String(password ?? "") === String(confirmPassword ?? "");
}

/**
 * Length validator.
 *
 * @param {*} value
 * @param {number} min
 * @param {number} max
 * @returns {boolean}
 */
export function validateLength(value, min, max) {
  const length = normalize(value).length;

  return length >= min && length <= max;
}

/**
 * URL validator.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function validateURL(value) {
  const url = normalize(value);

  if (!url) {
    return true;
  }

  try {
    new URL(url);

    return true;
  } catch {
    return false;
  }
}

/* --------------------------------------------------------
 * File Validators
 * ------------------------------------------------------ */

/**
 * Validate image MIME type.
 *
 * @param {File|null} file
 * @returns {boolean}
 */
export function validateImage(file) {
  if (!(file instanceof File)) {
    return false;
  }

  const allowedTypes = ["image/jpeg", "image/png", "image/webp", "image/gif"];

  return allowedTypes.includes(file.type);
}

/**
 * Validate file size.
 *
 * @param {File|null} file
 * @param {number} [maxSizeMB=5]
 * @returns {boolean}
 */
export function validateFileSize(file, maxSizeMB = 5) {
  if (!(file instanceof File)) {
    return false;
  }

  return file.size <= maxSizeMB * 1024 * 1024;
}

/* --------------------------------------------------------
 * Field Validators
 * ------------------------------------------------------ */

/**
 * Validate required field.
 *
 * @param {HTMLInputElement|HTMLTextAreaElement|HTMLSelectElement|null} field
 * @param {string} [message]
 * @returns {boolean}
 */
export function validateRequiredField(
  field,
  message = "This field is required.",
) {
  if (!field) {
    return false;
  }

  return setValidationState(field, validateRequired(getValue(field)), message);
}

/**
 * Validate email field.
 *
 * @param {HTMLInputElement|null} field
 * @returns {boolean}
 */
export function validateEmailField(field) {
  if (!field) {
    return false;
  }

  const value = getValue(field);

  if (!value) {
    return setValidationState(field, false, "Email is required.");
  }

  return setValidationState(
    field,
    validateEmail(value),
    "Enter a valid email address.",
  );
}

/**
 * Validate username field.
 *
 * @param {HTMLInputElement|null} field
 * @returns {boolean}
 */
export function validateUsernameField(field) {
  if (!field) {
    return false;
  }

  const value = getValue(field);

  if (!value) {
    return setValidationState(field, false, "Username is required.");
  }

  return setValidationState(
    field,
    validateUsername(value),
    "Username must be 3–30 characters and contain only letters, numbers, or underscores.",
  );
}

/**
 * Validate password field.
 *
 * @param {HTMLInputElement|null} field
 * @returns {boolean}
 */
export function validatePasswordField(field) {
  if (!field) {
    return false;
  }

  const value = getValue(field);

  if (!value) {
    return setValidationState(field, false, "Password is required.");
  }

  return setValidationState(
    field,
    validatePassword(value),
    "Password does not meet security requirements.",
  );
}

/**
 * Validate confirm password field.
 *
 * @param {HTMLInputElement|null} passwordField
 * @param {HTMLInputElement|null} confirmField
 * @returns {boolean}
 */
export function validateConfirmPasswordField(passwordField, confirmField) {
  if (!passwordField || !confirmField) {
    return false;
  }

  return setValidationState(
    confirmField,
    validateConfirmPassword(getValue(passwordField), getValue(confirmField)),
    "Passwords do not match.",
  );
}

/**
 * Validate URL field.
 *
 * @param {HTMLInputElement|null} field
 * @returns {boolean}
 */
export function validateURLField(field) {
  if (!field) {
    return false;
  }

  return setValidationState(
    field,
    validateURL(getValue(field)),
    "Enter a valid website URL.",
  );
}

/* --------------------------------------------------------
 * Generic Field Validators
 * ------------------------------------------------------ */

/**
 * Validate minimum length.
 *
 * @param {HTMLInputElement|HTMLTextAreaElement|null} field
 * @param {number} min
 * @param {string} message
 * @returns {boolean}
 */
export function validateMinLengthField(field, min, message) {
  if (!field) {
    return false;
  }

  const value = getValue(field);

  return setValidationState(field, value.length >= min, message);
}

/**
 * Validate maximum length.
 *
 * @param {HTMLInputElement|HTMLTextAreaElement|null} field
 * @param {number} max
 * @param {string} message
 * @returns {boolean}
 */
export function validateMaxLengthField(field, max, message) {
  if (!field) {
    return false;
  }

  const value = getValue(field);

  return setValidationState(field, value.length <= max, message);
}

/**
 * Validate length range.
 *
 * @param {HTMLInputElement|HTMLTextAreaElement|null} field
 * @param {number} min
 * @param {number} max
 * @param {string} message
 * @returns {boolean}
 */
export function validateLengthField(field, min, max, message) {
  if (!field) {
    return false;
  }

  return setValidationState(
    field,
    validateLength(getValue(field), min, max),
    message,
  );
}

/* --------------------------------------------------------
 * File Field Validators
 * ------------------------------------------------------ */

/**
 * Validate image upload field.
 *
 * @param {HTMLInputElement|null} field
 * @param {number} [maxSizeMB=5]
 * @returns {boolean}
 */
export function validateImageField(field, maxSizeMB = 5) {
  if (!(field instanceof HTMLInputElement)) {
    return false;
  }

  const file = field.files?.[0];

  if (!file) {
    return true;
  }

  if (!validateImage(file)) {
    return setValidationState(
      field,
      false,
      "Only JPG, PNG, WEBP and GIF images are allowed.",
    );
  }

  if (!validateFileSize(file, maxSizeMB)) {
    return setValidationState(
      field,
      false,
      `Image must be smaller than ${maxSizeMB} MB.`,
    );
  }

  return setValidationState(field, true, "");
}

/* --------------------------------------------------------
 * Form Validator
 * ------------------------------------------------------ */

/**
 * Validate multiple fields.
 *
 * Stops at the first invalid field.
 *
 * @param {Array<() => boolean>} validators
 * @returns {boolean}
 */
export function validateForm(validators) {
  for (const validate of validators) {
    if (!validate()) {
      return false;
    }
  }

  return true;
}

/* --------------------------------------------------------
 * Error Helpers
 * ------------------------------------------------------ */

/**
 * Clear validation state from a field.
 *
 * @param {HTMLElement|null} field
 */
export function clearValidation(field) {
  if (!field) {
    return;
  }

  clearFieldError(field);
}

/**
 * Mark field as valid.
 *
 * @param {HTMLElement|null} field
 */
export function markFieldValid(field) {
  if (!field) {
    return;
  }

  clearFieldError(field);
}

/**
 * Mark field as invalid.
 *
 * @param {HTMLElement|null} field
 * @param {string} message
 */
export function markFieldInvalid(field, message) {
  if (!field) {
    return;
  }

  showFieldError(field, message);
}
