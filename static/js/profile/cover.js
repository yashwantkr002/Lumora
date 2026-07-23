/*
===========================================================
File: static/js/profile/cover.js
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

    const coverInput =
        getElement("coverImage") || document.querySelector(
            "input[name='cover_image']"
        );

    const coverPreviewContainer =
        getElement("coverPreview");

    if (
        !coverInput ||
        !coverPreviewContainer
    ) {
        return;
    }

    /* --------------------------------------------------
     * State
     * -------------------------------------------------- */

    let currentFile = null;

    let previewURL = null;

    /* --------------------------------------------------
     * Preview
     * -------------------------------------------------- */

    let coverPreview =
        coverPreviewContainer.querySelector("img");

    if (!coverPreview) {

        coverPreview =
            document.createElement("img");

        coverPreview.className =
            "mt-4 w-full rounded-lg object-cover";

        coverPreview.style.display = "none";

        coverPreview.style.maxHeight =
            "300px";

        coverPreviewContainer.appendChild(
            coverPreview
        );

    }

    /* --------------------------------------------------
     * Crop Button
     * -------------------------------------------------- */

    let cropButton =
        coverPreviewContainer.querySelector(
            ".cover-crop-btn"
        ) || document.querySelector(".cover-crop-btn");

    if (!cropButton) {

        cropButton =
            document.createElement("button");

        cropButton.type = "button";

        cropButton.textContent =
            "Crop Image";

        cropButton.className =
            "cover-crop-btn mt-2 rounded-lg bg-primary px-4 py-2 text-white";

        cropButton.style.display =
            "none";

        coverPreviewContainer.appendChild(
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

        URL.revokeObjectURL(
            previewURL
        );

        previewURL = null;

    }

    function hidePreview() {

        clearPreviewURL();

        coverPreview.removeAttribute(
            "src"
        );

        coverPreview.style.display =
            "none";

        cropButton.style.display =
            "none";

    }

    function showPreview(file) {

        clearPreviewURL();

        previewURL =
            URL.createObjectURL(file);

        coverPreview.src =
            previewURL;

        coverPreview.style.display =
            "block";

        cropButton.style.display =
            "inline-flex";

    }

    function updateInputFile(file) {

        const dt =
            new DataTransfer();

        dt.items.add(file);

        coverInput.files =
            dt.files;

    }

    function validate(file) {

        clearFieldError(
            coverInput
        );

        if (
            !validateImage(file)
        ) {

            showFieldError(

                coverInput,

                "Please upload a valid image (JPEG, PNG, WebP, GIF)."

            );

            hidePreview();

            return false;

        }

        if (
            !validateFileSize(file, 10)
        ) {

            showFieldError(

                coverInput,

                "File size must be less than 10MB."

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

        coverInput,

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
     * Crop Cover
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

                    aspectRatio: 16 / 9,

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

                        updateInputFile(
                            croppedFile
                        );

                        showPreview(
                            croppedFile
                        );

                    },

                });

            } catch (error) {

                console.error(

                    "Cover crop failed:",

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