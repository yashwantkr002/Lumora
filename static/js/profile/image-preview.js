/*
===========================================================
File: static/js/profile/image-preview.js
===========================================================

PURPOSE

Generic image preview utility for file uploads.

Features

✓ Preview Generation
✓ Validation
✓ Error Handling

===========================================================
*/

"use strict";

/**
 * Show image preview from file input.
 *
 * @param {File} file
 * @param {HTMLImageElement} previewElement
 * @returns {Promise<void>}
 */
export async function showImagePreview(file, previewElement) {
  if (!file || !previewElement) {
    return;
  }

  return new Promise((resolve) => {
    const reader = new FileReader();

    reader.onload = (event) => {
      previewElement.src = event.target?.result || "";
      previewElement.style.display = "block";
      resolve();
    };

    reader.onerror = () => {
      previewElement.style.display = "none";
      resolve();
    };

    reader.readAsDataURL(file);
  });
}

/**
 * Clear image preview.
 *
 * @param {HTMLImageElement} previewElement
 */
export function clearImagePreview(previewElement) {
  if (previewElement) {
    previewElement.src = "";
    previewElement.style.display = "none";
  }
}
