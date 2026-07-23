/*
===========================================================
File: static/js/auth/auth.js
===========================================================

PURPOSE

Authentication utility functions for Lumora.

Utilities

- togglePassword: Toggle password field visibility
- getPasswordStrength: Evaluate password strength
- passwordsMatch: Compare two password values

===========================================================
*/

"use strict";

/* --------------------------------------------------------
 * Password Visibility
 * ------------------------------------------------------ */

/**
 * Toggle password visibility.
 *
 * Updates both the input type and icon visibility.
 *
 * @param {HTMLInputElement} passwordInput
 * @param {HTMLElement} toggleButton
 */
export function togglePassword(passwordInput, toggleButton) {
  if (!passwordInput || !toggleButton) {
    return;
  }

  const isPassword = passwordInput.type === "password";

  // Toggle input type
  passwordInput.type = isPassword ? "text" : "password";

  // Toggle icon classes
  const icon = toggleButton.querySelector("i") || toggleButton;

  if (isPassword) {
    // Show eye-slash icon (password visible)
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    // Show eye icon (password hidden)
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  }
}

/* --------------------------------------------------------
 * Password Strength Evaluation
 * ------------------------------------------------------ */

/**
 * Evaluate password strength.
 *
 * Returns an object with:
 * - score: 0-5 (strength level)
 * - label: User-friendly strength label
 * - color: Tailwind color class for the strength bar
 *
 * @param {string} password
 * @returns {{score: number, label: string, color: string}}
 */
export function getPasswordStrength(password) {
  if (!password) {
    return {
      score: 0,
      label: "No password",
      color: "bg-gray-300",
    };
  }

  let score = 0;

  // Length checks
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;

  // Character type checks
  if (/[a-z]/.test(password)) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^a-zA-Z0-9]/.test(password)) score++;

  // Normalize score to 0-5
  score = Math.min(5, Math.ceil(score / 1.2));

  let label = "Weak";
  let color = "bg-red-500";

  switch (score) {
    case 0:
    case 1:
      label = "Weak";
      color = "bg-red-500";
      break;

    case 2:
      label = "Fair";
      color = "bg-orange-500";
      break;

    case 3:
      label = "Good";
      color = "bg-yellow-500";
      break;

    case 4:
      label = "Strong";
      color = "bg-blue-500";
      break;

    case 5:
      label = "Very Strong";
      color = "bg-green-500";
      break;
  }

  return { score, label, color };
}

/* --------------------------------------------------------
 * Password Matching
 * ------------------------------------------------------ */

/**
 * Check if two passwords match.
 *
 * @param {string} password1
 * @param {string} password2
 * @returns {boolean}
 */
export function passwordsMatch(password1, password2) {
  return (
    password1 &&
    password2 &&
    password1.trim() === password2.trim() &&
    password1.length > 0
  );
}
