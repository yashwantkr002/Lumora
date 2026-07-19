/**
 * ===========================================================
 * Django CSRF Utilities
 * ===========================================================
 */

export function getCSRFToken() {

    return document.cookie
        .split("; ")
        .find(cookie => cookie.startsWith("csrftoken="))
        ?.split("=")[1] ?? "";

}