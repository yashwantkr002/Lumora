/*
===========================================================
File: static/js/posts/create-post.service.js
===========================================================

Purpose

Server communication for Create Post.

Responsibilities

✓ Create posts
✓ Upload FormData
✓ Normalize API responses
✓ Normalize API errors

Does NOT

✗ Handle UI
✗ Render previews
✗ Manage DOM
✗ Show toast notifications

Dependencies

✓ http.js

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
  CREATE: "/posts/create/",
});

/* ---------------------------------------------------------
 * Error Classes
 * ------------------------------------------------------ */

export class CreatePostServiceError extends Error {
  constructor(message, code = "CREATE_POST_SERVICE_ERROR") {
    super(message);

    this.name = "CreatePostServiceError";

    this.code = code;
  }
}

export class CreatePostRequestError extends CreatePostServiceError {
  constructor(message) {
    super(
      message,

      "CREATE_POST_REQUEST_ERROR",
    );
  }
}

/* ---------------------------------------------------------
 * Create Post Service
 * ------------------------------------------------------ */

export class CreatePostService {
  /* ---------------------------------------------------------
   * Public API
   * ------------------------------------------------------ */

  /**
   * Create a new post.
   *
   * @param {FormData} formData
   * @returns {Promise<any>}
   */
  async create(formData) {
    try {
      const response = await http.post(
        API.CREATE,

        formData,
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
   * @returns {CreatePostServiceError}
   */
  #normalizeError(error) {
    if (error instanceof CreatePostServiceError) {
      return error;
    }

    const message =
      error?.data?.message ?? error?.message ?? "Unable to create post.";

    return new CreatePostRequestError(message);
  }
  /* ---------------------------------------------------------
   * Configuration
   * ------------------------------------------------------ */

  /**
   * Build request options.
   *
   * @private
   *
   * @param {Object} [options={}]
   * @returns {RequestInit}
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
   * Public API
   * ------------------------------------------------------ */

  /**
   * Create a new post with request options.
   *
   * @param {FormData} formData
   * @param {Object} [options={}]
   * @returns {Promise<any>}
   */
  async create(formData, options = {}) {
    try {
      const response = await http.post(
        API.CREATE,

        formData,

        this.#buildRequestOptions(options),
      );

      return this.#normalizeResponse(response);
    } catch (error) {
      throw this.#normalizeError(error);
    }
  }
  /* ---------------------------------------------------------
   * Future API
   * ------------------------------------------------------ */

  /**
   * Get a single post.
   *
   * @param {number|string} postId
   * @returns {Promise<never>}
   */
  async get(postId) {
    throw new Error("CreatePostService.get() is not implemented.");
  }

  /**
   * Update a post.
   *
   * @param {number|string} postId
   * @param {FormData} formData
   * @returns {Promise<never>}
   */
  async update(postId, formData) {
    throw new Error("CreatePostService.update() is not implemented.");
  }

  /**
   * Delete a post.
   *
   * @param {number|string} postId
   * @returns {Promise<never>}
   */
  async delete(postId) {
    throw new Error("CreatePostService.delete() is not implemented.");
  }
}
