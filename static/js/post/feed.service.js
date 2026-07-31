/*
===========================================================
File: static/js/posts/feed.service.js
===========================================================

Purpose

Server communication for Feed.

Responsibilities

✓ Fetch feed
✓ Pagination
✓ Normalize responses
✓ Normalize errors

Does NOT

✗ Render UI
✗ Manipulate DOM
✗ Handle infinite scroll
✗ Manage post cards

===========================================================
*/

"use strict";

/* ---------------------------------------------------------
 * Imports
 * ------------------------------------------------------ */

import * as http from "../core/http.js";

/* ---------------------------------------------------------
 * API Endpoints
 * ------------------------------------------------------ */

const API = Object.freeze({
  FEED: "/posts/feed/",
});

/* ---------------------------------------------------------
 * Error Classes
 * ------------------------------------------------------ */

export class FeedServiceError extends Error {
  constructor(message, code = "FEED_SERVICE_ERROR") {
    super(message);

    this.name = "FeedServiceError";
    this.code = code;
  }
}

export class FeedRequestError extends FeedServiceError {
  constructor(message) {
    super(message, "FEED_REQUEST_ERROR");
  }
}

/* ---------------------------------------------------------
 * Feed Service
 * ------------------------------------------------------ */

export class FeedService {
  /* ---------------------------------------------------------
   * Public API
   * ------------------------------------------------------ */

  /**
   * Fetch feed.
   *
   * @param {Object} [options={}]
   * @returns {Promise<any>}
   */
  async getFeed(options = {}) {
    const { page = 1, limit = 10, sort, cursor, filters = {} } = options;

    const params = new URLSearchParams({
      page,
      limit,
    });

    if (sort) {
      params.set("sort", sort);
    }

    if (cursor) {
      params.set("cursor", cursor);
    }

    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        params.set(key, value);
      }
    });

    try {
      const response = await http.get(
        `${API.FEED}?${params.toString()}`,

        this.#buildRequestOptions(options),
      );

      return this.#normalizeResponse(response);
    } catch (error) {
      throw this.#normalizeError(error);
    }
  }

  /* ---------------------------------------------------------
   * Response Helpers
   * ------------------------------------------------------ */

  /**
   * Normalize API response.
   *
   * @private
   *
   * @param {*} response
   * @returns {*}
   */
  #normalizeResponse(response) {
    return response;
  }

  /**
   * Normalize request errors.
   *
   * @private
   *
   * @param {Error} error
   * @returns {FeedServiceError}
   */
  #normalizeError(error) {
    if (error instanceof FeedServiceError) {
      return error;
    }

    const message =
      error?.data?.message ?? error?.message ?? "Unable to load feed.";

    return new FeedRequestError(message);
  }
  /* ---------------------------------------------------------
   * Configuration
   * ------------------------------------------------------ */

  /**
   * Build request options.
   *
   * @private
   *
   * @param {Object} options
   * @returns {Object}
   */
  #buildRequestOptions(options = {}) {
    return {
      timeout: options.timeout ?? 30000,

      headers: {
        ...options.headers,
      },
    };
  }
  /* ---------------------------------------------------------
   * Future API
   * ------------------------------------------------------ */

  /**
   * Refresh the feed.
   *
   * @param {Object} [options={}]
   * @returns {Promise<any>}
   */
  async refresh(options = {}) {
    return this.getFeed({
      ...options,

      page: 1,
    });
  }

  /**
   * Load next page.
   *
   * @param {number} page
   * @param {Object} [options={}]
   * @returns {Promise<any>}
   */
  async loadMore(page, options = {}) {
    return this.getFeed({
      ...options,

      page,
    });
  }

  /**
   * Get a single post.
   *
   * Reserved for V2.
   *
   * @param {number|string} postId
   * @returns {Promise<never>}
   */
  async getPost(postId) {
    throw new Error("FeedService.getPost() is not implemented.");
  }
}
