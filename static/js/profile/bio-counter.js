/*
===========================================================
File: static/js/profile/bio-counter.js
===========================================================

PURPOSE

Real-time character counter for bio textarea.

Features

✓ Real-time Character Count
✓ Visual Feedback
✓ Max Limit Warning
✓ Smooth Updates

===========================================================
*/

"use strict";

import { getElement, ready, on, setText } from "../core/dom.js";

const MAX_BIO_LENGTH = 500;

ready(() => {
  /* --------------------------------------------------
   * Elements
   * -------------------------------------------------- */

  const bioField = getElement("bio");
  const bioCounter = getElement("bioCounter");

  if (!(bioField instanceof HTMLTextAreaElement) || !bioCounter) {
    return;
  }

  /* --------------------------------------------------
   * Update Counter
   * -------------------------------------------------- */

  function updateCounter() {
    const length = bioField.value.length;
    const remaining = MAX_BIO_LENGTH - length;

    // Update counter text
    setText(bioCounter, `${remaining} characters remaining`);

    // Add warning class when near limit
    if (remaining <= 50) {
      bioCounter.className = "text-sm font-medium text-orange-500";
    } else if (remaining <= 0) {
      bioCounter.className = "text-sm font-medium text-red-500";
    } else {
      bioCounter.className = "text-sm text-slate-500";
    }
  }

  /* --------------------------------------------------
   * Initial Count
   * -------------------------------------------------- */

  updateCounter();

  /* --------------------------------------------------
   * Listen for Changes
   * -------------------------------------------------- */

  on(bioField, "input", updateCounter);
});
