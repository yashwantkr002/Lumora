/*
===========================================================
File: static/js/core/http.js
===========================================================

PURPOSE

Reusable HTTP client for Lumora.

Features

- Fetch API
- JSON
- FormData
- CSRF
- Timeout
- AbortController
- Query Params
- Automatic Error Handling

Used By

- Authentication
- Profile
- Posts
- Stories
- Comments
- Chat
- Notifications

===========================================================
*/

"use strict";

/* --------------------------------------------------------
 * Constants
 * ------------------------------------------------------ */

const DEFAULT_TIMEOUT = 30000;

const DEFAULT_HEADERS = {
  Accept: "application/json",
  "X-Requested-With": "XMLHttpRequest",
};

/* --------------------------------------------------------
 * CSRF
 * ------------------------------------------------------ */

/**
 * Get CSRF token from cookie.
 *
 * @returns {string}
 */
export function getCSRFToken() {
  const cookie = document.cookie
    .split("; ")
    .find((cookie) => cookie.startsWith("csrftoken="));

  return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
}

/* --------------------------------------------------------
 * URL Helpers
 * ------------------------------------------------------ */

/**
 * Build URL with query parameters.
 *
 * @param {string} url
 * @param {Object} [params]
 * @returns {string}
 */
function buildURL(url, params = {}) {
  const target = new URL(url, window.location.origin);

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null) {
      return;
    }

    target.searchParams.append(key, value);
  });

  return target.toString();
}

/* --------------------------------------------------------
 * Timeout
 * ------------------------------------------------------ */

/**
 * Create AbortController timeout.
 *
 * @param {number} timeout
 * @returns {{
 * controller: AbortController,
 * timeoutId: number
 * }}
 */
function createTimeout(timeout) {
  const controller = new AbortController();

  const timeoutId = window.setTimeout(() => {
    controller.abort();
  }, timeout);

  return {
    controller,
    timeoutId,
  };
}

/* --------------------------------------------------------
 * Response Helpers
 * ------------------------------------------------------ */

/**
 * Parse response.
 *
 * @param {Response} response
 * @returns {Promise<any>}
 */
async function parseResponse(response) {
  const type = response.headers.get("content-type") ?? "";

  if (type.includes("application/json")) {
    return await response.json();
  }

  if (type.includes("text/")) {
    return await response.text();
  }

  return await response.blob();
}
/* --------------------------------------------------------
 * Core Request
 * ------------------------------------------------------ */

/**
 * Perform HTTP request.
 *
 * @param {string} url
 * @param {RequestInit} [options={}]
 * @returns {Promise<any>}
 */
export async function request(url, options = {}) {
  const {
    timeout = DEFAULT_TIMEOUT,
    params = {},
    headers = {},
    body,
    ...config
  } = options;

  const { controller, timeoutId } = createTimeout(timeout);

  const requestHeaders = new Headers({
    ...DEFAULT_HEADERS,
    ...headers,
  });

  let requestBody = body;

  if (body instanceof FormData) {
    requestHeaders.delete("Content-Type");
  } else if (body && typeof body === "object") {
    requestHeaders.set("Content-Type", "application/json");

    requestBody = JSON.stringify(body);
  }

  const method = (config.method ?? "GET").toUpperCase();

  if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
    requestHeaders.set("X-CSRFToken", getCSRFToken());
  }

  try {
    const response = await fetch(
      buildURL(url, params),

      {
        ...config,

        method,

        headers: requestHeaders,

        body: requestBody,

        signal: controller.signal,
      },
    );

    clearTimeout(timeoutId);

    const data = await parseResponse(response);

    if (!response.ok) {
      const error = new Error(response.statusText);

      error.status = response.status;

      error.data = data;

      throw error;
    }

    return data;
  } catch (error) {
    clearTimeout(timeoutId);

    if (error.name === "AbortError") {
      throw new Error("Request timeout.");
    }

    throw error;
  }
}

/* --------------------------------------------------------
 * HTTP Methods
 * ------------------------------------------------------ */

/**
 * GET request.
 *
 * @param {string} url
 * @param {Object} [params]
 * @param {RequestInit} [options]
 * @returns {Promise<any>}
 */
export function get(url, params = {}, options = {}) {
  return request(url, {
    ...options,
    method: "GET",
    params,
  });
}

/**
 * POST request.
 *
 * @param {string} url
 * @param {*} body
 * @param {RequestInit} [options]
 * @returns {Promise<any>}
 */
export function post(url, body, options = {}) {
  return request(url, {
    ...options,
    method: "POST",
    body,
  });
}

/**
 * PUT request.
 *
 * @param {string} url
 * @param {*} body
 * @param {RequestInit} [options]
 * @returns {Promise<any>}
 */
export function put(url, body, options = {}) {
  return request(url, {
    ...options,
    method: "PUT",
    body,
  });
}

/**
 * PATCH request.
 *
 * @param {string} url
 * @param {*} body
 * @param {RequestInit} [options]
 * @returns {Promise<any>}
 */
export function patch(url, body, options = {}) {
  return request(url, {
    ...options,
    method: "PATCH",
    body,
  });
}

/**
 * DELETE request.
 *
 * @param {string} url
 * @param {*} body
 * @param {RequestInit} [options]
 * @returns {Promise<any>}
 */
export function del(url, body = null, options = {}) {
  return request(url, {
    ...options,
    method: "DELETE",
    body,
  });
}
