/**
 * ===========================================================
 * File: static/js/save/toggle.js
 * ===========================================================
 *
 * PURPOSE
 *
 * Handles bookmark toggle.
 *
 * ===========================================================
 */

import Ajax from "../core/ajax.js";
import Toast from "../common/toast.js";


document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeSaveButtons();

    },
);


/**
 * -----------------------------------------------------------
 * Initialize
 * -----------------------------------------------------------
 */

function initializeSaveButtons() {

    const buttons = document.querySelectorAll(
        "[data-save-button]",
    );

    buttons.forEach(

        button => {

            button.addEventListener(
                "click",
                handleSaveToggle,
            );

        },

    );

}


/**
 * -----------------------------------------------------------
 * Toggle Bookmark
 * -----------------------------------------------------------
 */

async function handleSaveToggle(
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

        updateSaveUI(
            button,
            data,
        );

        Toast.success(

            data.saved
                ? "Post saved."
                : "Bookmark removed.",

        );

    }

    catch (error) {

        console.error(
            error,
        );

        Toast.error(

            error.message ||
            "Unable to save post.",

        );

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

function updateSaveUI(
    button,
    data,
) {

    const icon = button.querySelector(
        "[data-save-icon]",
    );

    if (data.saved) {

        icon.classList.remove(
            "fa-regular",
        );

        icon.classList.add(
            "fa-solid",
        );

    }

    else {

        icon.classList.remove(
            "fa-solid",
        );

        icon.classList.add(
            "fa-regular",
        );

    }

}