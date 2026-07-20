/*
===========================================================
File: static/js/core/validation.js
===========================================================

PURPOSE

Reusable validation utilities for Lumora.

Used By

- Authentication
- Profile
- Posts
- Comments
- Stories
- Chat

===========================================================
*/

"use strict";

/**
 * Normalize a value into a trimmed string.
 *
 * @param {*} value
 * @returns {string}
 */
function normalize(value) {
    return String(value ?? "").trim();
}

/**
 * Check whether a value is empty.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function isEmpty(value) {
    return normalize(value) === "";
}

/**
 * Validate required field.
 *
 * @param {*} value
 * @returns {boolean}
 */
export function validateRequired(value) {
    return !isEmpty(value);
}

/**
 * Validate email address.
 *
 * @param {*} email
 * @returns {boolean}
 */
export function validateEmail(email) {

    const regex =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return regex.test(normalize(email));
}

/**
 * Validate username.
 *
 * Rules
 * - 3 to 30 characters
 * - Letters
 * - Numbers
 * - Underscore
 *
 * @param {*} username
 * @returns {boolean}
 */
export function validateUsername(username) {

    const regex =
        /^[a-zA-Z0-9_]{3,30}$/;

    return regex.test(normalize(username));
}

/**
 * Validate password.
 *
 * Rules
 * - Minimum 8 characters
 * - One uppercase
 * - One lowercase
 * - One number
 * - One special character
 *
 * @param {*} password
 * @returns {boolean}
 */
export function validatePassword(password) {

    const regex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&^#()_+\-=[\]{};':"\\|,.<>/?]).{8,}$/;

    return regex.test(String(password ?? ""));
}

/**
 * Validate password confirmation.
 *
 * @param {*} password
 * @param {*} confirmPassword
 * @returns {boolean}
 */
export function validateConfirmPassword(
    password,
    confirmPassword,
) {

    return String(password ?? "") ===
        String(confirmPassword ?? "");
}

/**
 * Validate string length.
 *
 * @param {*} value
 * @param {number} min
 * @param {number} max
 * @returns {boolean}
 */
export function validateLength(
    value,
    min,
    max,
) {

    const length = normalize(value).length;

    return length >= min && length <= max;
}

/**
 * Validate file size.
 *
 * @param {File|null} file
 * @param {number} maxSizeMB
 * @returns {boolean}
 */
export function validateFileSize(
    file,
    maxSizeMB = 5,
) {

    if (!(file instanceof File)) {
        return false;
    }

    return file.size <= maxSizeMB * 1024 * 1024;
}

/**
 * Validate image file type.
 *
 * @param {File|null} file
 * @returns {boolean}
 */
export function validateImage(file) {

    if (!(file instanceof File)) {
        return false;
    }

    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    ];

    return allowedTypes.includes(file.type);
}