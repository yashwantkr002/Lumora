/**
 * ===========================================================
 * File: static/js/like/toggle.js
 * ===========================================================
 *
 * PURPOSE
 *
 * Handles AJAX like toggling.
 *
 * ===========================================================
 */

import Ajax from "../core/ajax.js";
import Toast from "../common/toast.js";

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeLikeButtons();

    },
);


/**
 * -----------------------------------------------------------
 * Initialize
 * -----------------------------------------------------------
 */

function initializeLikeButtons() {

    const buttons = document.querySelectorAll(
        "[data-like-button]",
    );

    buttons.forEach(

        button => {

            button.addEventListener(
                "click",
                handleLikeToggle,
            );

        },

    );

}


/**
 * -----------------------------------------------------------
 * Toggle Like
 * -----------------------------------------------------------
 */

async function handleLikeToggle(
    event,
) {

    const button = event.currentTarget;

    try {

        button.disabled = true;

        const data = await Ajax.post(

            button.dataset.url,

        );

        if (!data.success) {

            throw new Error(
                data.message,
            );

        }

        updateLikeUI(
            button,
            data,
        );

    }

    catch (error) {

        console.error(
            error,
        );

        // TODO:
        // Replace with Toast component.

    }

    finally {

        button.disabled = false;

    }

}


/**
 * -----------------------------------------------------------
 * Update UI
 * -----------------------------------------------------------
 */

function updateLikeUI(
    button,
    data,
) {

    const icon = button.querySelector(
        "[data-like-icon]",
    );

    const total = document.querySelector(

        `[data-like-total="${button.dataset.postId}"]`

    );

    if (data.liked) {

        icon.classList.remove(
            "fa-regular",
        );

        icon.classList.add(
            "fa-solid",
            "text-red-500",
        );

    }

    else {

        icon.classList.remove(
            "fa-solid",
            "text-red-500",
        );

        icon.classList.add(
            "fa-regular",
        );

    }

    if (total) {

        total.textContent =
            data.likes_count;

    }

}