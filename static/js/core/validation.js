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
 * Check whether a value is empty.
 *
 * @param {string} value
 * @returns {boolean}
 */
export function isEmpty(value) {
    return value.trim() === "";
}

/**
 * Validate required field.
 *
 * @param {string} value
 * @returns {boolean}
 */
export function validateRequired(value) {
    return !isEmpty(value);
}

/**
 * Validate email address.
 *
 * @param {string} email
 * @returns {boolean}
 */
export function validateEmail(email) {

    const regex =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return regex.test(email.trim());
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
 * @param {string} username
 * @returns {boolean}
 */
export function validateUsername(username) {

    const regex =
        /^[a-zA-Z0-9_]{3,30}$/;

    return regex.test(username.trim());
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
 * @param {string} password
 * @returns {boolean}
 */
export function validatePassword(password) {

    const regex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&^#()_+\-=[\]{};':"\\|,.<>/?]).{8,}$/;

    return regex.test(password);
}

/**
 * Validate password confirmation.
 *
 * @param {string} password
 * @param {string} confirmPassword
 * @returns {boolean}
 */
export function validateConfirmPassword(
    password,
    confirmPassword,
) {
    return password === confirmPassword;
}

/**
 * Validate string length.
 *
 * @param {string} value
 * @param {number} min
 * @param {number} max
 * @returns {boolean}
 */
export function validateLength(
    value,
    min,
    max,
) {

    const length = value.trim().length;

    return length >= min && length <= max;
}

/**
 * Check if file size is valid.
 *
 * @param {File} file
 * @param {number} maxSizeMB
 * @returns {boolean}
 */
export function validateFileSize(
    file,
    maxSizeMB = 5,
) {

    if (!file) {
        return false;
    }

    return file.size <= maxSizeMB * 1024 * 1024;
}

/**
 * Validate image file type.
 *
 * @param {File} file
 * @returns {boolean}
 */
export function validateImage(file) {

    if (!file) {
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