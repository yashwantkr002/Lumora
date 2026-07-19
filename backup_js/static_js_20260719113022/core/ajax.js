/**
 * ===========================================================
 * File: static/js/core/ajax.js
 * ===========================================================
 *
 * PURPOSE
 *
 * Shared AJAX helper.
 *
 * ===========================================================
 */

import {
    getCSRFToken,
} from "./csrf.js";


class Ajax {

    /**
     * POST Request
     */

    static async post(
        url,
        body = {},
    ) {

        const response = await fetch(
            url,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },

                body: JSON.stringify(
                    body,
                ),
            },
        );

        return response.json();

    }

    /**
     * GET Request
     */

    static async get(
        url,
    ) {

        const response = await fetch(
            url,
        );

        return response.json();

    }

}


export default Ajax;