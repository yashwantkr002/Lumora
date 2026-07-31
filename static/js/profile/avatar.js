/*
===========================================================
File: static/js/profile/avatar.js
PART 1 / 2
===========================================================
*/

"use strict";

import {
    getElement,
    ready,
    on,
    showFieldError,
    clearFieldError,
} from "../core/dom.js";

import {
    validateImage,
    validateFileSize,
} from "../core/validation.js";

import {
    openCropModal,
} from "./crop-ui.js";

ready(() => {

    /* --------------------------------------------------
     * Elements
     * -------------------------------------------------- */

    const avatarInput =
        getElement("avatar") || document.querySelector("input[name='avatar']");

    const avatarPreviewContainer =
        getElement("avatarPreview");

    if (
        !avatarInput ||
        !avatarPreviewContainer
    ) {
        return;
    }

    /* --------------------------------------------------
     * State
     * -------------------------------------------------- */

    let currentFile = null;

    let previewURL = null;

    /* --------------------------------------------------
     * Preview Image
     * -------------------------------------------------- */

    let avatarPreview =
        avatarPreviewContainer.querySelector("img");

    if (!avatarPreview) {

        avatarPreview =
            document.createElement("img");

        avatarPreview.className =
            "mt-4 max-w-xs rounded-lg";

        avatarPreview.style.display = "none";

        avatarPreviewContainer.appendChild(
            avatarPreview
        );

    }

    /* --------------------------------------------------
     * Crop Button
     * -------------------------------------------------- */

    let cropButton =
        avatarPreviewContainer.querySelector(
            ".avatar-crop-btn"
        ) || document.querySelector(".avatar-crop-btn");

    if (!cropButton) {

        cropButton =
            document.createElement("button");

        cropButton.type = "button";

        cropButton.textContent = "Crop Image";

        cropButton.className =
            "avatar-crop-btn mt-2 rounded-lg bg-primary px-4 py-2 text-white";

        cropButton.style.display = "none";

        avatarPreviewContainer.appendChild(
            cropButton
        );

    }

    /* --------------------------------------------------
     * Helpers
     * -------------------------------------------------- */

    function clearPreviewURL() {

        if (!previewURL) {
            return;
        }

        URL.revokeObjectURL(previewURL);

        previewURL = null;

    }

    function hidePreview() {

        clearPreviewURL();

        avatarPreview.removeAttribute("src");

        avatarPreview.style.display = "none";

        cropButton.style.display = "none";

    }

    function showPreview(file) {

        clearPreviewURL();

        previewURL =
            URL.createObjectURL(file);

        avatarPreview.src = previewURL;

        avatarPreview.style.display = "block";

        cropButton.style.display = "inline-flex";

    }

    function updateInputFile(file) {

        const dt =
            new DataTransfer();

        dt.items.add(file);

        avatarInput.files =
            dt.files;

    }

    function validate(file) {

        clearFieldError(
            avatarInput
        );

        if (
            !validateImage(file)
        ) {

            showFieldError(

                avatarInput,

                "Please upload a valid image (JPEG, PNG, WebP, GIF)."

            );

            hidePreview();

            return false;

        }

        if (
            !validateFileSize(file, 5)
        ) {

            showFieldError(

                avatarInput,

                "File size must be less than 5MB."

            );

            hidePreview();

            return false;

        }

        return true;

    }

    /* --------------------------------------------------
     * File Change
     * -------------------------------------------------- */

    on(

        avatarInput,

        "change",

        event => {

            const file =
                event.target.files?.[0];

            if (!file) {

                currentFile = null;

                hidePreview();

                return;

            }

            if (!validate(file)) {

                currentFile = null;

                return;

            }

            currentFile = file;

            showPreview(file);

        }

    );
        /* --------------------------------------------------
     * Crop Avatar
     * -------------------------------------------------- */

    on(

        cropButton,

        "click",

        async event => {

            event.preventDefault();

            event.stopPropagation();

            if (!currentFile) {
                return;
            }

            try {

                await openCropModal({

                    imageFile: currentFile,

                    aspectRatio: 1,

                    onSave: async blob => {

                        const croppedFile = new File(

                            [blob],

                            currentFile.name,

                            {

                                type: blob.type,

                                lastModified: Date.now(),

                            }

                        );

                        currentFile = croppedFile;

                        updateInputFile(croppedFile);

                        showPreview(croppedFile);

                    },

                });

            } catch (error) {

                console.error(
                    "Avatar crop failed:",
                    error
                );

            }

        }

    );

    /* --------------------------------------------------
     * Cleanup
     * -------------------------------------------------- */

    window.addEventListener(

        "beforeunload",

        clearPreviewURL

    );

});