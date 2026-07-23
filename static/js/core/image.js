/*
===========================================================
File: static/js/core/image.js
===========================================================

PURPOSE

Reusable image utilities for Lumora.

Used By

✓ Avatar
✓ Cover
✓ Posts
✓ Stories
✓ Chat
✓ Media Upload

===========================================================
*/

"use strict";

/* ---------------------------------------------------------
 * Imports
 * ------------------------------------------------------ */

import { clamp, isBlob, isFile, isImageFile, isImageElement } from "./utils.js";

/* ---------------------------------------------------------
 * Constants
 * ------------------------------------------------------ */

export const IMAGE_TYPES = Object.freeze([
  "image/jpeg",
  "image/png",
  "image/webp",
  "image/gif",
  "image/avif",
]);

export const IMAGE_DEFAULTS = Object.freeze({
  maxSize: 5 * 1024 * 1024,

  maxWidth: 2048,

  maxHeight: 2048,

  quality: 0.9,

  outputType: "image/webp",
});

/* ---------------------------------------------------------
 * Validation
 * ------------------------------------------------------ */

/**
 * Validate an image file.
 *
 * @param {File} file
 * @param {Object} [options]
 * @param {number} [options.maxSize]
 * @param {string[]} [options.allowedTypes]
 *
 * @returns {{
 * valid:boolean,
 * code:string|null,
 * message:string|null
 * }}
 */
export function validateImage(
  file,
  { maxSize = IMAGE_DEFAULTS.maxSize, allowedTypes = IMAGE_TYPES } = {},
) {
  if (!isFile(file)) {
    return {
      valid: false,

      code: "INVALID_FILE",

      message: "Expected a File object.",
    };
  }

  if (!isImageFile(file)) {
    return {
      valid: false,

      code: "NOT_IMAGE",

      message: "Selected file is not an image.",
    };
  }

  if (!allowedTypes.includes(file.type)) {
    return {
      valid: false,

      code: "INVALID_TYPE",

      message: "Unsupported image format.",
    };
  }

  if (file.size > maxSize) {
    return {
      valid: false,

      code: "FILE_TOO_LARGE",

      message: `Maximum allowed size is ${Math.round(maxSize / 1024 / 1024)} MB.`,
    };
  }

  return {
    valid: true,

    code: null,

    message: null,
  };
}

/* ---------------------------------------------------------
 * Read Image
 * ------------------------------------------------------ */

/**
 * Read image as Data URL.
 *
 * @param {File} file
 *
 * @returns {Promise<string>}
 */
export function readImage(file) {
  const validation = validateImage(file);

  if (!validation.valid) {
    return Promise.reject(new Error(validation.message));
  }

  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = () => {
      resolve(String(reader.result));
    };

    reader.onerror = () => {
      reject(new Error("Unable to read image."));
    };

    reader.readAsDataURL(file);
  });
}

/* ---------------------------------------------------------
 * Load Image
 * ------------------------------------------------------ */

/**
 * Load an image source.
 *
 * @param {string} source
 *
 * @returns {Promise<HTMLImageElement>}
 */
export function loadImage(source) {
  return new Promise((resolve, reject) => {
    const image = new Image();

    image.decoding = "async";

    image.onload = () => {
      resolve(image);
    };

    image.onerror = () => {
      reject(new Error("Unable to load image."));
    };

    image.src = source;
  });
}

/* ---------------------------------------------------------
 * Image Dimensions
 * ------------------------------------------------------ */

/**
 * Get image dimensions.
 *
 * @param {File|Blob|string|HTMLImageElement} source
 *
 * @returns {Promise<{
 * width:number,
 * height:number
 * }>}
 */
export async function getImageDimensions(source) {
  if (isImageElement(source)) {
    return {
      width: source.naturalWidth,

      height: source.naturalHeight,
    };
  }

  let imageSource = source;

  let objectURL = null;

  if (isFile(source) || isBlob(source)) {
    objectURL = URL.createObjectURL(source);

    imageSource = objectURL;
  }

  try {
    const image = await loadImage(imageSource);

    return {
      width: image.naturalWidth,

      height: image.naturalHeight,
    };
  } finally {
    if (objectURL) {
      URL.revokeObjectURL(objectURL);
    }
  }
}

/* ---------------------------------------------------------
 * Aspect Ratio
 * ------------------------------------------------------ */

/**
 * Calculate aspect ratio.
 *
 * @param {number} width
 * @param {number} height
 *
 * @returns {number}
 */
export function calculateAspectRatio(width, height) {
  if (width <= 0 || height <= 0) {
    throw new Error("Width and height must be greater than zero.");
  }

  return clamp(width / height, 0, Number.MAX_SAFE_INTEGER);
}

/* ---------------------------------------------------------
 * Part 2
 *
 * Next:
 *
 * ✓ Canvas Helpers
 * ✓ Resize Engine
 * ✓ Scale Calculation
 * ✓ High Quality Rendering
 *
 * ------------------------------------------------------ */
/* ---------------------------------------------------------
 * Private Canvas Helpers
 * ------------------------------------------------------ */

/**
 * Create canvas.
 *
 * @param {number} width
 * @param {number} height
 *
 * @returns {HTMLCanvasElement}
 */
function createCanvas(width, height) {
  const canvas = document.createElement("canvas");

  canvas.width = Math.max(1, Math.round(width));

  canvas.height = Math.max(1, Math.round(height));

  return canvas;
}

/**
 * Get canvas context.
 *
 * @param {HTMLCanvasElement} canvas
 *
 * @returns {CanvasRenderingContext2D}
 */
function getCanvasContext(canvas) {
  const context = canvas.getContext("2d", {
    alpha: true,
    willReadFrequently: false,
  });

  if (!context) {
    throw new Error("Unable to create canvas context.");
  }

  context.imageSmoothingEnabled = true;

  context.imageSmoothingQuality = "high";

  return context;
}

/**
 * Calculate resized dimensions.
 *
 * @param {number} width
 * @param {number} height
 * @param {number} maxWidth
 * @param {number} maxHeight
 * @param {boolean} preserveAspectRatio
 *
 * @returns {{
 * width:number,
 * height:number
 * }}
 */
function calculateDimensions(
  width,
  height,
  maxWidth,
  maxHeight,
  preserveAspectRatio = true,
) {
  if (!preserveAspectRatio) {
    return {
      width: Math.round(maxWidth),

      height: Math.round(maxHeight),
    };
  }

  const scale = Math.min(
    maxWidth / width,

    maxHeight / height,

    1,
  );

  return {
    width: Math.round(width * scale),

    height: Math.round(height * scale),
  };
}

/**
 * Draw image on canvas.
 *
 * @param {CanvasRenderingContext2D} context
 * @param {CanvasImageSource} image
 * @param {number} width
 * @param {number} height
 * @param {string|null} background
 */
function drawImage(context, image, width, height, background = null) {
  context.clearRect(0, 0, width, height);

  if (background) {
    context.fillStyle = background;

    context.fillRect(0, 0, width, height);
  }

  context.drawImage(image, 0, 0, width, height);
}

/* ---------------------------------------------------------
 * Resize Engine
 * ------------------------------------------------------ */

/**
 * Resize image.
 *
 * @param {HTMLImageElement} image
 * @param {Object} [options]
 * @param {number} [options.maxWidth]
 * @param {number} [options.maxHeight]
 * @param {boolean} [options.preserveAspectRatio]
 * @param {string|null} [options.background]
 *
 * @returns {HTMLCanvasElement}
 */
export function resizeImage(
  image,
  {
    maxWidth = IMAGE_DEFAULTS.maxWidth,

    maxHeight = IMAGE_DEFAULTS.maxHeight,

    preserveAspectRatio = true,

    background = null,
  } = {},
) {
  if (!isImageElement(image)) {
    throw new Error("Expected HTMLImageElement.");
  }

  const {
    width,

    height,
  } = calculateDimensions(
    image.naturalWidth,

    image.naturalHeight,

    maxWidth,

    maxHeight,

    preserveAspectRatio,
  );

  const canvas = createCanvas(width, height);

  const context = getCanvasContext(canvas);

  drawImage(
    context,

    image,

    width,

    height,

    background,
  );

  return canvas;
}

/* ---------------------------------------------------------
 * Canvas Information
 * ------------------------------------------------------ */

/**
 * Get canvas dimensions.
 *
 * @param {HTMLCanvasElement} canvas
 *
 * @returns {{
 * width:number,
 * height:number
 * }}
 */
export function getCanvasDimensions(canvas) {
  return {
    width: canvas.width,

    height: canvas.height,
  };
}

/**
 * Check if canvas is empty.
 *
 * @param {HTMLCanvasElement} canvas
 *
 * @returns {boolean}
 */
export function isCanvasEmpty(canvas) {
  return canvas.width === 0 || canvas.height === 0;
}

/* ---------------------------------------------------------
 * PART 3
 *
 * Next
 *
 * ✓ canvasToBlob()
 * ✓ compressImage()
 * ✓ blobToFile()
 * ✓ createObjectURL()
 * ✓ revokeObjectURL()
 *
 * ------------------------------------------------------ */
/* ---------------------------------------------------------
 * Canvas → Blob
 * ------------------------------------------------------ */

/**
 * Convert canvas to Blob.
 *
 * @param {HTMLCanvasElement} canvas
 * @param {Object} [options]
 * @param {string} [options.type]
 * @param {number} [options.quality]
 *
 * @returns {Promise<Blob>}
 */
export function canvasToBlob(
  canvas,
  { type = IMAGE_DEFAULTS.outputType, quality = IMAGE_DEFAULTS.quality } = {},
) {
  return new Promise((resolve, reject) => {
    if (!(canvas instanceof HTMLCanvasElement)) {
      reject(new Error("Expected HTMLCanvasElement."));

      return;
    }

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          reject(new Error("Failed to create Blob."));

          return;
        }

        resolve(blob);
      },

      type,

      clamp(quality, 0, 1),
    );
  });
}

/* ---------------------------------------------------------
 * Compression
 * ------------------------------------------------------ */

/**
 * Compress canvas.
 *
 * @param {HTMLCanvasElement} canvas
 * @param {Object} [options]
 * @param {string} [options.type]
 * @param {number} [options.quality]
 *
 * @returns {Promise<Blob>}
 */
export async function compressImage(
  canvas,
  { type = IMAGE_DEFAULTS.outputType, quality = IMAGE_DEFAULTS.quality } = {},
) {
  return canvasToBlob(
    canvas,

    {
      type,

      quality,
    },
  );
}

/* ---------------------------------------------------------
 * Blob → File
 * ------------------------------------------------------ */

/**
 * Convert Blob to File.
 *
 * @param {Blob} blob
 * @param {Object} options
 * @param {string} options.filename
 * @param {string} [options.type]
 * @param {number} [options.lastModified]
 *
 * @returns {File}
 */
export function blobToFile(
  blob,
  { filename, type = blob.type, lastModified = Date.now() },
) {
  if (!(blob instanceof Blob)) {
    throw new Error("Expected Blob.");
  }

  return new File(
    [blob],

    filename,

    {
      type,

      lastModified,
    },
  );
}

/* ---------------------------------------------------------
 * Object URL
 * ------------------------------------------------------ */

/**
 * Create object URL.
 *
 * @param {Blob|File} file
 *
 * @returns {string}
 */
export function createObjectURL(file) {
  if (!(file instanceof Blob)) {
    throw new Error("Expected Blob or File.");
  }

  return URL.createObjectURL(file);
}

/**
 * Revoke object URL.
 *
 * @param {string} url
 */
export function revokeObjectURL(url) {
  if (!url) {
    return;
  }

  URL.revokeObjectURL(url);
}

/* ---------------------------------------------------------
 * Image Conversion
 * ------------------------------------------------------ */

/**
 * Convert image to Blob.
 *
 * @param {HTMLImageElement} image
 * @param {Object} [options]
 *
 * @returns {Promise<Blob>}
 */
export async function imageToBlob(image, options = {}) {
  const canvas = resizeImage(
    image,

    options,
  );

  return compressImage(
    canvas,

    options,
  );
}

/**
 * Convert image to File.
 *
 * @param {HTMLImageElement} image
 * @param {Object} options
 *
 * @returns {Promise<File>}
 */
export async function imageToFile(image, options) {
  const blob = await imageToBlob(
    image,

    options,
  );

  return blobToFile(
    blob,

    {
      filename: options.filename ?? "image.webp",

      type: blob.type,
    },
  );
}

/* ---------------------------------------------------------
 * Part 4
 *
 * Next
 *
 * ✓ DataURL helpers
 * ✓ Base64 helpers
 * ✓ Export object
 * ✓ Final cleanup
 * ------------------------------------------------------ */
/* ---------------------------------------------------------
 * Data URL Helpers
 * ------------------------------------------------------ */

/**
 * Convert Blob to Data URL.
 *
 * @param {Blob} blob
 *
 * @returns {Promise<string>}
 */
export function blobToDataURL(blob) {
  if (!isBlob(blob)) {
    return Promise.reject(new Error("Expected Blob."));
  }

  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = () => {
      resolve(String(reader.result));
    };

    reader.onerror = () => {
      reject(new Error("Unable to convert Blob to Data URL."));
    };

    reader.readAsDataURL(blob);
  });
}

/**
 * Convert File to Data URL.
 *
 * @param {File} file
 *
 * @returns {Promise<string>}
 */
export function fileToDataURL(file) {
  return readImage(file);
}

/* ---------------------------------------------------------
 * File Information
 * ------------------------------------------------------ */

/**
 * Format bytes into readable string.
 *
 * @param {number} bytes
 *
 * @returns {string}
 */
export function formatFileSize(bytes) {
  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(2)} KB`;
  }

  return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
}

/**
 * Get file extension.
 *
 * @param {File} file
 *
 * @returns {string}
 */
export function getFileExtension(file) {
  if (!isFile(file)) {
    return "";
  }

  const index = file.name.lastIndexOf(".");

  if (index === -1) {
    return "";
  }

  return file.name.substring(index + 1).toLowerCase();
}

/**
 * Check supported image type.
 *
 * @param {File} file
 *
 * @returns {boolean}
 */
export function isSupportedImage(file) {
  return isImageFile(file) && IMAGE_TYPES.includes(file.type);
}

/* ---------------------------------------------------------
 * Image Information
 * ------------------------------------------------------ */

/**
 * Get image metadata.
 *
 * @param {File|Blob|string|HTMLImageElement} source
 *
 * @returns {Promise<Object>}
 */
export async function getImageMetadata(source) {
  const {
    width,

    height,
  } = await getImageDimensions(source);

  return {
    width,

    height,

    aspectRatio: calculateAspectRatio(width, height),

    orientation: width >= height ? "landscape" : "portrait",
  };
}

/* ---------------------------------------------------------
 * Default Export
 * ------------------------------------------------------ */

const ImageUtils = Object.freeze({
  validateImage,

  readImage,

  loadImage,

  getImageDimensions,

  calculateAspectRatio,

  resizeImage,

  compressImage,

  canvasToBlob,

  blobToFile,

  imageToBlob,

  imageToFile,

  createObjectURL,

  revokeObjectURL,

  blobToDataURL,

  fileToDataURL,

  formatFileSize,

  getFileExtension,

  isSupportedImage,

  getImageMetadata,
});

export default ImageUtils;
