/*
===========================================================
File: static/js/profile/profile.js
===========================================================

PURPOSE

Handles profile page interactions.

Features

✓ Follow Button Loading
✓ Unfollow Button Loading
✓ Message Button Loading
✓ Copy Profile URL
✓ Native Share API
✓ Browser Back Restore
✓ Smooth Scroll To Posts

===========================================================
*/

"use strict";

import { ready, on, getElement, setText } from "../core/dom.js";

import {
  copyToClipboard,
  setButtonLoading,
  resetButtonLoading,
} from "../core/utils.js";

let followButton;
let unfollowButton;
let messageButton;
let copyProfileButton;
let shareProfileButton;
let profilePosts;

ready(() => {
  //--------------------------------------------------
  // Elements
  //--------------------------------------------------

  followButton = getElement("followButton");

  unfollowButton = getElement("unfollowButton");

  messageButton = getElement("messageButton");

  copyProfileButton = getElement("copyProfileButton");

  shareProfileButton = getElement("shareProfileButton");

  profilePosts = getElement("profilePosts");

  //--------------------------------------------------
  // Follow Button
  //--------------------------------------------------

  if (followButton) {
    on(followButton, "click", () => {
      setButtonLoading(followButton, "Following...");
    });
  }

  //--------------------------------------------------
  // Unfollow Button
  //--------------------------------------------------

  if (unfollowButton) {
    on(unfollowButton, "click", () => {
      setButtonLoading(unfollowButton, "Unfollowing...");
    });
  }

  //--------------------------------------------------
  // Message Button
  //--------------------------------------------------

  if (messageButton) {
    on(messageButton, "click", () => {
      setButtonLoading(messageButton, "Opening...");
    });
  }

  //--------------------------------------------------
  // Copy Profile URL
  //--------------------------------------------------

  if (copyProfileButton) {
    on(copyProfileButton, "click", async () => {
      const success = await copyToClipboard(window.location.href);

      setText(copyProfileButton, success ? "Copied!" : "Copy Failed");

      setTimeout(() => {
        setText(copyProfileButton, "Copy Profile");
      }, 2000);
    });
  }

  //--------------------------------------------------
  // Share Profile
  //--------------------------------------------------

  if (shareProfileButton) {
    on(shareProfileButton, "click", async () => {
      if (navigator.share) {
        try {
          await navigator.share({
            title: document.title,

            url: window.location.href,
          });

          return;
        } catch {
          // User cancelled sharing.
        }
      }

      const success = await copyToClipboard(window.location.href);

      setText(shareProfileButton, success ? "Copied!" : "Share");

      setTimeout(() => {
        setText(shareProfileButton, "Share");
      }, 2000);
    });
  }

  //--------------------------------------------------
  // Browser Back Restore
  //--------------------------------------------------

  on(window, "pageshow", () => {
    if (followButton) {
      resetButtonLoading(followButton);
    }

    if (unfollowButton) {
      resetButtonLoading(unfollowButton);
    }

    if (messageButton) {
      resetButtonLoading(messageButton);
    }
  });
});

/* --------------------------------------------------
 * Smooth Scroll To Posts
 * -------------------------------------------------- */

export function scrollToPosts() {
  if (!profilePosts) {
    return;
  }

  profilePosts.scrollIntoView({
    behavior: "smooth",

    block: "start",
  });
}
