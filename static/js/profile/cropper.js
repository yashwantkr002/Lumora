/*
===========================================================
File: static/js/profile/cropper.js
PART 1 / 2
===========================================================
*/

"use strict";

/* ---------------------------------------------------------
 * Constants
 * ------------------------------------------------------- */

const DEFAULT_OPTIONS = {
  aspectRatio: 1,
  quality: 0.92,
  mimeType: "image/jpeg",
  maxCanvasSize: 1200,
};

const DEFAULT_STATE = {
  scale: 1,
  rotation: 0,
  flipX: false,
  flipY: false,

  offsetX: 0,
  offsetY: 0,

  cropX: 0,
  cropY: 0,
  cropWidth: 0,
  cropHeight: 0,

  brightness: 100,
  contrast: 100,
  saturation: 100,

  history: [],
  isDirty: false,
};

/* ---------------------------------------------------------
 * Utilities
 * ------------------------------------------------------- */

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function degreesToRadians(angle) {
  return (angle * Math.PI) / 180;
}

function cloneState(state) {
  return {
    scale: state.scale,

    rotation: state.rotation,

    flipX: state.flipX,

    flipY: state.flipY,

    offsetX: state.offsetX,

    offsetY: state.offsetY,

    cropX: state.cropX,

    cropY: state.cropY,

    cropWidth: state.cropWidth,

    cropHeight: state.cropHeight,

    brightness: state.brightness,

    contrast: state.contrast,

    saturation: state.saturation,

    history: [...state.history],

    isDirty: state.isDirty,
  };
}

function resetCanvas(ctx, canvas) {
  ctx.setTransform(1, 0, 0, 1, 0, 0);

  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

/* ---------------------------------------------------------
 * Image Loader
 * ------------------------------------------------------- */

function loadImage(file) {
  return new Promise((resolve, reject) => {
    if (!(file instanceof File)) {
      reject(new Error("Invalid image file."));

      return;
    }

    const reader = new FileReader();

    reader.onload = (event) => {
      const image = new Image();

      image.onload = () => resolve(image);

      image.onerror = () => reject(new Error("Failed to load image."));

      image.src = event.target?.result ?? "";
    };

    reader.onerror = () => reject(new Error("Unable to read image."));

    reader.readAsDataURL(file);
  });
}

/* ---------------------------------------------------------
 * Canvas Size
 * ------------------------------------------------------- */

function calculateCanvasSize(image, aspectRatio, maxCanvasSize) {
  let width = image.width;

  let height = image.height;

  if (width / height > aspectRatio) {
    width = height * aspectRatio;
  } else {
    height = width / aspectRatio;
  }

  const scale = Math.min(1, maxCanvasSize / Math.max(width, height));

  return {
    width: Math.round(width * scale),

    height: Math.round(height * scale),
  };
}

/* ---------------------------------------------------------
 * Cropper Factory
 * ------------------------------------------------------- */

export async function createCropper(
  file,

  aspectRatio = 1,

  options = {},
) {
  const settings = {
    ...DEFAULT_OPTIONS,

    aspectRatio,

    ...options,
  };

  const image = await loadImage(file);

  const size = calculateCanvasSize(
    image,

    settings.aspectRatio,

    settings.maxCanvasSize,
  );

  const canvas = document.createElement("canvas");

  canvas.width = size.width;

  canvas.height = size.height;

  const ctx = canvas.getContext("2d");

  if (!ctx) {
    throw new Error("Unable to create canvas context.");
  }

  const state = cloneState(DEFAULT_STATE);
  state.cropWidth = image.width;

  state.cropHeight = image.height;

  const fitScale = Math.min(
    canvas.width / image.width,

    canvas.height / image.height,
  );

  state.scale = fitScale;

  function render() {
    resetCanvas(ctx, canvas);

    ctx.save();

    ctx.filter = `
brightness(${state.brightness}%)
contrast(${state.contrast}%)
saturate(${state.saturation}%)
`;

    ctx.translate(
      canvas.width / 2 + state.offsetX,

      canvas.height / 2 + state.offsetY,
    );

    ctx.scale(
      state.flipX ? -1 : 1,

      state.flipY ? -1 : 1,
    );

    ctx.rotate(degreesToRadians(state.rotation));

    const drawWidth = image.width * state.scale;

    const drawHeight = image.height * state.scale;

    ctx.drawImage(
      image,
      state.cropX,
      state.cropY,
      state.cropWidth,
      state.cropHeight,

      -drawWidth / 2,

      -drawHeight / 2,

      drawWidth,

      drawHeight,
    );
    state.isDirty = true;
    ctx.restore();
  }

  render();

  return {
    canvas,

    image,

    state,

    render,

    zoom(value) {
      state.scale = clamp(value, 0.2, 5);

      render();
    },
    pan(dx, dy) {
      state.offsetX += dx;

      state.offsetY += dy;

      render();
    },

    rotate(angle) {
      state.rotation = (state.rotation + angle) % 360;

      render();
    },

    setRotation(angle) {
      state.rotation = angle;

      render();
    },

    flipHorizontal() {
      state.flipX = !state.flipX;

      render();
    },

    flipVertical() {
      state.flipY = !state.flipY;

      render();
    },

    setBrightness(value) {
      state.brightness = clamp(value, 0, 300);

      render();
    },

    setContrast(value) {
      state.contrast = clamp(value, 0, 300);

      render();
    },

    setSaturation(value) {
      state.saturation = clamp(value, 0, 300);

      render();
    },
    reset() {
      Object.assign(state, cloneState(DEFAULT_STATE));

      render();
    },
    destroy() {
      canvas.width = 0;

      canvas.height = 0;

      image.src = "";

      state.history.length = 0;
    },

    exportBlob(quality = settings.quality, mimeType = settings.mimeType) {
      return new Promise((resolve) => {
        canvas.toBlob(
          (blob) => resolve(blob),

          mimeType,

          quality,
        );
      });
    },

    exportDataURL(quality = settings.quality, mimeType = settings.mimeType) {
      return canvas.toDataURL(mimeType, quality);
    },

    getState() {
      return cloneState(state);
    },

    setState(nextState = {}) {
      Object.assign(state, nextState);

      render();
    },
  };
}

/* ---------------------------------------------------------
 * Standalone Helpers
 * ------------------------------------------------------- */

export function cropImage(sourceCanvas, x, y, width, height) {
  if (!(sourceCanvas instanceof HTMLCanvasElement)) {
    return null;
  }

  const canvas = document.createElement("canvas");

  canvas.width = width;

  canvas.height = height;

  const ctx = canvas.getContext("2d");

  if (!ctx) {
    return null;
  }

  ctx.drawImage(
    sourceCanvas,

    x,
    y,
    width,
    height,

    0,
    0,
    width,
    height,
  );

  return canvas;
}

export function scaleImageOnCanvas(cropper, scale) {
  if (!cropper) {
    return;
  }

  cropper.zoom(scale);
}

export function rotateImageOnCanvas(cropper, angle) {
  if (!cropper) {
    return;
  }

  cropper.setRotation(angle);
}

export function flipImageHorizontal(cropper) {
  if (!cropper) {
    return;
  }

  cropper.flipHorizontal();
}

export function flipImageVertical(cropper) {
  if (!cropper) {
    return;
  }

  cropper.flipVertical();
}

export function applyFiltersToCanvas(cropper, filters = {}) {
  if (!cropper) {
    return;
  }

  if (typeof filters.brightness === "number") {
    cropper.setBrightness(filters.brightness);
  }

  if (typeof filters.contrast === "number") {
    cropper.setContrast(filters.contrast);
  }

  if (typeof filters.saturation === "number") {
    cropper.setSaturation(filters.saturation);
  }
}

export function exportCanvasAsBlob(
  canvas,
  quality = 0.92,
  mimeType = "image/jpeg",
) {
  if (!(canvas instanceof HTMLCanvasElement)) {
    return Promise.resolve(null);
  }

  return new Promise((resolve) => {
    canvas.toBlob(
      (blob) => resolve(blob),

      mimeType,

      quality,
    );
  });
}

export function exportCanvasAsDataURL(
  canvas,
  quality = 0.92,
  mimeType = "image/jpeg",
) {
  if (!(canvas instanceof HTMLCanvasElement)) {
    return "";
  }

  return canvas.toDataURL(mimeType, quality);
}
