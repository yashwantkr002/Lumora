/*
===========================================================
File: static/js/core/upload.js
===========================================================

Reusable Upload Engine

Used By

✓ Avatar Upload
✓ Cover Upload
✓ Post Upload
✓ Story Upload
✓ Chat Upload
✓ Future Media Uploads

===========================================================
*/

"use strict";

/* ---------------------------------------------------------
 * Imports
 * ------------------------------------------------------ */

import { isFile, isArray, isObject } from "./utils.js";

import { validateImage } from "./image.js";

import { getCSRFToken } from "./http.js";

/* ---------------------------------------------------------
 * Constants
 * ------------------------------------------------------ */

export const UPLOAD_STATUS = Object.freeze({
  IDLE: "idle",

  UPLOADING: "uploading",

  SUCCESS: "success",

  ERROR: "error",

  CANCELLED: "cancelled",
});

export const DEFAULT_UPLOAD_OPTIONS = Object.freeze({
  fieldName: "file",

  multiple: false,

  timeout: 30000,

  retries: 0,

  retryDelay: 1000,

  withCredentials: true,

  headers: {},
});

/* ---------------------------------------------------------
 * Upload Errors
 * ------------------------------------------------------ */

export class UploadError extends Error {
  constructor(message, code = "UPLOAD_ERROR") {
    super(message);

    this.name = "UploadError";

    this.code = code;
  }
}

export class UploadTimeoutError extends UploadError {
  constructor() {
    super(
      "Upload timed out.",

      "UPLOAD_TIMEOUT",
    );

    this.name = "UploadTimeoutError";
  }
}

export class UploadCancelledError extends UploadError {
  constructor() {
    super(
      "Upload cancelled.",

      "UPLOAD_CANCELLED",
    );

    this.name = "UploadCancelledError";
  }
}

export class UploadValidationError extends UploadError {
  constructor(message) {
    super(
      message,

      "UPLOAD_VALIDATION",
    );

    this.name = "UploadValidationError";
  }
}

/* ---------------------------------------------------------
 * Validation
 * ------------------------------------------------------ */

/**
 * Validate upload input.
 *
 * @param {File|File[]} files
 * @param {Object} options
 *
 * @returns {File[]}
 */
function validateUpload(
  files,

  options = {},
) {
  let list;

  if (isFile(files)) {
    list = [files];
  } else if (Array.isArray(files)) {
    list = files;
  } else {
    throw new UploadValidationError("Expected File or File[].");
  }

  if (!list.length) {
    throw new UploadValidationError("No files selected.");
  }

  for (const file of list) {
    if (!isFile(file)) {
      throw new UploadValidationError("Invalid file.");
    }

    if (options.image === true) {
      const result = validateImage(file);

      if (!result.valid) {
        throw new UploadValidationError(result.message);
      }
    }
  }

  return list;
}

/* ---------------------------------------------------------
 * FormData
 * ------------------------------------------------------ */

/**
 * Create FormData.
 *
 * @param {File[]} files
 * @param {Object} options
 *
 * @returns {FormData}
 */
export function createFormData(
  files,

  options = {},
) {
  const {
    fieldName = DEFAULT_UPLOAD_OPTIONS.fieldName,

    multiple = DEFAULT_UPLOAD_OPTIONS.multiple,

    data = {},
  } = options;

  const formData = new FormData();

  if (multiple) {
    files.forEach((file) => {
      formData.append(
        fieldName,

        file,
      );
    });
  } else {
    formData.append(
      fieldName,

      files[0],
    );
  }

  if (isObject(data)) {
    Object.entries(data)

      .forEach(([key, value]) => {
        formData.append(
          key,

          value,
        );
      });
  }

  return formData;
}

/* ---------------------------------------------------------
 * Private Helpers
 * ------------------------------------------------------ */

/**
 * Create upload headers.
 *
 * @param {Object} headers
 *
 * @returns {Object}
 */
function buildHeaders(headers = {}) {
  return {
    "X-CSRFToken": getCSRFToken(),

    ...headers,
  };
}

/* ---------------------------------------------------------
 * Part 2
 *
 * Next:
 *
 * ✓ XMLHttpRequest Engine
 * ✓ Progress Tracking
 * ✓ Timeout
 * ✓ AbortController
 * ✓ Promise Wrapper
 *
 * ------------------------------------------------------ */
/* ---------------------------------------------------------
 * Upload Request
 * ------------------------------------------------------ */

/**
 * Upload using XMLHttpRequest.
 *
 * @param {string} url
 * @param {FormData} formData
 * @param {Object} options
 *
 * @returns {Promise<Object>}
 */
function uploadRequest(url, formData, options = {}) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    const {
      timeout = DEFAULT_UPLOAD_OPTIONS.timeout,

      withCredentials = DEFAULT_UPLOAD_OPTIONS.withCredentials,

      headers = {},

      signal = null,

      onProgress = null,
    } = options;

    xhr.open("POST", url, true);

    xhr.timeout = timeout;

    xhr.withCredentials = withCredentials;

    const requestHeaders = buildHeaders(headers);

    Object.entries(requestHeaders).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        xhr.setRequestHeader(key, value);
      }
    });

    /* ---------------------------------------------
     * Upload Progress
     * ------------------------------------------ */

    if (typeof onProgress === "function") {
      xhr.upload.onprogress = (event) => {
        if (!event.lengthComputable) {
          return;
        }

        const percentage = Math.round((event.loaded / event.total) * 100);

        onProgress({
          loaded: event.loaded,

          total: event.total,

          percentage,
        });
      };
    }

    /* ---------------------------------------------
     * Success
     * ------------------------------------------ */

    xhr.onload = () => {
      const response = {
        status: xhr.status,

        statusText: xhr.statusText,

        headers: xhr.getAllResponseHeaders(),

        data: null,
      };

      try {
        response.data = xhr.responseText ? JSON.parse(xhr.responseText) : null;
      } catch {
        response.data = xhr.responseText;
      }

      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(response);

        return;
      }

      reject(
        new UploadError(
          response.statusText || "Upload failed.",

          String(xhr.status),
        ),
      );
    };

    /* ---------------------------------------------
     * Network Error
     * ------------------------------------------ */

    xhr.onerror = () => {
      reject(
        new UploadError(
          "Network error.",

          "NETWORK_ERROR",
        ),
      );
    };

    /* ---------------------------------------------
     * Timeout
     * ------------------------------------------ */

    xhr.ontimeout = () => {
      reject(new UploadTimeoutError());
    };

    /* ---------------------------------------------
     * Abort
     * ------------------------------------------ */

    xhr.onabort = () => {
      reject(new UploadCancelledError());
    };

    /* ---------------------------------------------
     * AbortController Support
     * ------------------------------------------ */

    if (signal) {
      if (signal.aborted) {
        xhr.abort();

        return;
      }

      signal.addEventListener(
        "abort",

        () => {
          xhr.abort();
        },

        {
          once: true,
        },
      );
    }

    xhr.send(formData);
  });
}

/* ---------------------------------------------------------
 * Upload Helpers
 * ------------------------------------------------------ */

/**
 * Create AbortController.
 *
 * @returns {AbortController}
 */
export function createUploadController() {
  return new AbortController();
}

/**
 * Cancel upload.
 *
 * @param {AbortController} controller
 */
export function cancelUpload(controller) {
  if (controller instanceof AbortController && !controller.signal.aborted) {
    controller.abort();
  }
}

/* ---------------------------------------------------------
 * Part 3
 *
 * Next
 *
 * ✓ uploadFile()
 * ✓ uploadFiles()
 * ✓ uploadImage()
 * ✓ Retry Engine
 * ✓ UploadManager Class
 *
 * ------------------------------------------------------ */

/* ---------------------------------------------------------
 * Retry Helper
 * ------------------------------------------------------ */

/**
 * Delay execution.
 *
 * @param {number} milliseconds
 *
 * @returns {Promise<void>}
 */
function delay(milliseconds) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, milliseconds);
  });
}

/* ---------------------------------------------------------
 * Upload Single File
 * ------------------------------------------------------ */

/**
 * Upload a single file.
 *
 * @param {string} url
 * @param {File} file
 * @param {Object} [options]
 *
 * @returns {Promise<Object>}
 */
export async function uploadFile(url, file, options = {}) {
  const files = validateUpload(file, options);

  const {
    retries = DEFAULT_UPLOAD_OPTIONS.retries,

    retryDelay = DEFAULT_UPLOAD_OPTIONS.retryDelay,
  } = options;

  const formData = createFormData(files, options);

  let attempt = 0;
  let lastError = null;

  while (attempt <= retries) {
    try {
      return await uploadRequest(url, formData, options);
    } catch (error) {
      lastError = error;

      if (
        error instanceof UploadCancelledError ||
        error instanceof UploadValidationError
      ) {
        throw error;
      }

      if (attempt === retries) {
        break;
      }

      await delay(retryDelay);

      attempt++;
    }
  }

  throw lastError;
}

/* ---------------------------------------------------------
 * Upload Multiple Files
 * ------------------------------------------------------ */

/**
 * Upload multiple files.
 *
 * @param {string} url
 * @param {File[]} files
 * @param {Object} [options]
 *
 * @returns {Promise<Object>}
 */
export async function uploadFiles(url, files, options = {}) {
  const validatedFiles = validateUpload(files, options);

  const formData = createFormData(validatedFiles, {
    ...options,
    multiple: true,
  });

  return uploadRequest(url, formData, options);
}

/* ---------------------------------------------------------
 * Upload Image
 * ------------------------------------------------------ */

/**
 * Upload validated image.
 *
 * @param {string} url
 * @param {File} file
 * @param {Object} [options]
 *
 * @returns {Promise<Object>}
 */
export async function uploadImage(url, file, options = {}) {
  return uploadFile(url, file, {
    ...options,
    image: true,
  });
}

/* ---------------------------------------------------------
 * Upload Manager
 * ------------------------------------------------------ */

export class UploadManager {
  constructor() {
    this.controller = null;

    this.status = UPLOAD_STATUS.IDLE;
  }

  /**
   * Upload file.
   *
   * @param {string} url
   * @param {File} file
   * @param {Object} options
   *
   * @returns {Promise<Object>}
   */
  async upload(url, file, options = {}) {
    this.controller = createUploadController();

    this.status = UPLOAD_STATUS.UPLOADING;

    try {
      const response = await uploadFile(url, file, {
        ...options,
        signal: this.controller.signal,
      });

      this.status = UPLOAD_STATUS.SUCCESS;

      return response;
    } catch (error) {
      if (error instanceof UploadCancelledError) {
        this.status = UPLOAD_STATUS.CANCELLED;
      } else {
        this.status = UPLOAD_STATUS.ERROR;
      }

      throw error;
    }
  }

  /**
   * Cancel upload.
   */
  cancel() {
    cancelUpload(this.controller);
  }

  /**
   * Reset manager.
   */
  reset() {
    this.controller = null;

    this.status = UPLOAD_STATUS.IDLE;
  }

  /**
   * Check upload state.
   */
  isUploading() {
    return this.status === UPLOAD_STATUS.UPLOADING;
  }
}

/* ---------------------------------------------------------
 * Part 4
 *
 * Next
 *
 * ✓ Batch Upload Queue
 * ✓ Event Hooks
 * ✓ Default Export
 * ✓ Final Cleanup
 *
 * ------------------------------------------------------ */
/* ---------------------------------------------------------
 * Upload Queue
 * ------------------------------------------------------ */

export class UploadQueue {
  constructor() {
    this.queue = [];
  }

  /**
   * Add upload task.
   *
   * @param {Function} task
   */
  add(task) {
    this.queue.push(task);
  }

  /**
   * Clear queue.
   */
  clear() {
    this.queue.length = 0;
  }

  /**
   * Execute uploads sequentially.
   *
   * @returns {Promise<Array>}
   */
  async start() {
    const results = [];

    for (const task of this.queue) {
      results.push(await task());
    }

    return results;
  }
}

/* ---------------------------------------------------------
 * Upload Events
 * ------------------------------------------------------ */

class UploadEvents {
  constructor() {
    this.events = new Map();
  }

  on(name, callback) {
    if (!this.events.has(name)) {
      this.events.set(name, []);
    }

    this.events

      .get(name)

      .push(callback);
  }

  off(name, callback) {
    const listeners = this.events.get(name);

    if (!listeners) {
      return;
    }

    this.events.set(
      name,

      listeners.filter((listener) => listener !== callback),
    );
  }

  emit(name, payload) {
    const listeners = this.events.get(name);

    if (!listeners) {
      return;
    }

    for (const listener of listeners) {
      listener(payload);
    }
  }
}

/* ---------------------------------------------------------
 * Event Driven Upload Manager
 * ------------------------------------------------------ */

export class EventUploadManager extends UploadManager {
  constructor() {
    super();

    this.events = new UploadEvents();
  }

  on(event, callback) {
    this.events.on(
      event,

      callback,
    );
  }

  off(event, callback) {
    this.events.off(
      event,

      callback,
    );
  }

  async upload(
    url,

    file,

    options = {},
  ) {
    this.events.emit(
      "beforeUpload",

      file,
    );

    try {
      const response = await super.upload(
        url,

        file,

        {
          ...options,

          onProgress: (progress) => {
            options.onProgress?.(progress);

            this.events.emit(
              "progress",

              progress,
            );
          },
        },
      );

      this.events.emit(
        "success",

        response,
      );

      this.events.emit(
        "complete",

        response,
      );

      return response;
    } catch (error) {
      this.events.emit(
        "error",

        error,
      );

      throw error;
    }
  }
}

/* ---------------------------------------------------------
 * Default Upload Manager
 * ------------------------------------------------------ */

export const uploadManager = new EventUploadManager();

/* ---------------------------------------------------------
 * Default Export
 * ------------------------------------------------------ */

const Upload = Object.freeze({
  uploadFile,

  uploadFiles,

  uploadImage,

  createFormData,

  createUploadController,

  cancelUpload,

  UploadManager,

  EventUploadManager,

  UploadQueue,

  uploadManager,

  UploadError,

  UploadTimeoutError,

  UploadCancelledError,

  UploadValidationError,
});

export default Upload;
