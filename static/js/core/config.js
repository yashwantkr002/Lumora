/**
 * ===========================================================
 * File: static/js/core/config.js
 * ===========================================================
 *
 * Purpose:
 * Global application configuration.
 *
 * Used By:
 * - api.js
 * - upload.service.js
 * - notification.service.js
 * - bootstrap.js
 *
 * ===========================================================
 */

export const AppConfig = Object.freeze({

    APP_NAME: "Lumora",

    VERSION: "1.0.0",

    DEBUG: document.documentElement.dataset.debug === "true",

    API_PREFIX: "/",

    REQUEST_TIMEOUT: 30000,

    MAX_UPLOAD_FILES: 10,

    MAX_VIDEO_FILES: 1,

    ACCEPTED_IMAGE_TYPES: [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    ],

    ACCEPTED_VIDEO_TYPES: [
        "video/mp4",
        "video/webm",
        "video/quicktime",
    ],

});