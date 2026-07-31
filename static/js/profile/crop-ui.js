/*===========================================================
File: static/js/profile/crop-ui.js
========================================================== */

"use strict";

import { createCropper } from "./cropper.js";

let cropper = null;

let modal = null;
let previewContainer = null;
let previewCanvas = null;

let fileInput = null;

let saveButton = null;
let cancelButton = null;
let resetButton = null;

let zoomSlider = null;
let brightnessSlider = null;
let contrastSlider = null;
let saturationSlider = null;

let rotateLeftButton = null;
let rotateRightButton = null;

let flipHorizontalButton = null;
let flipVerticalButton = null;

let cleanupCallbacks = [];

function qs(selector) {
  return modal.querySelector(selector);
}

function addCleanup(callback) {
  cleanupCallbacks.push(callback);
}

function cleanup() {
  while (cleanupCallbacks.length) {
    const fn = cleanupCallbacks.pop();

    try {
      fn?.();
    } catch (error) {
      console.error(error);
    }
  }

  cleanupCallbacks = [];
}

function closeModal() {
  cleanup();

  cropper?.destroy();

  cropper = null;

  if (!modal) return;

  modal.classList.remove("show");

  modal.classList.add("hidden");

  modal.setAttribute("aria-hidden", "true");

  previewContainer.innerHTML = "";
}

function escHandler(event) {
  if (event.key === "Escape") {
    closeModal();
  }
}

function outsideClickHandler(event) {
  if (event.target === modal) {
    closeModal();
  }
}

function bindSlider(slider, callback) {
  if (!slider) return;

  const handler = (event) => {
    callback(Number(event.target.value));
  };

  slider.addEventListener("input", handler);

  addCleanup(() => slider.removeEventListener("input", handler));
}

function bindButton(button, callback) {
  if (!button) return;

  button.addEventListener("click", callback);

  addCleanup(() => button.removeEventListener("click", callback));
}

function updateCanvas() {
  if (!cropper) return;

  previewContainer.innerHTML = "";

  previewContainer.appendChild(cropper.canvas);

  let lastX = 0;
  let lastY = 0;
  let dragging = false;

  const pointerDown = (event) => {
    dragging = true;

    lastX = event.clientX;

    lastY = event.clientY;

    cropper.canvas.setPointerCapture(event.pointerId);
  };

  const pointerMove = (event) => {
    if (!dragging) return;

    const dx = event.clientX - lastX;

    const dy = event.clientY - lastY;

    lastX = event.clientX;

    lastY = event.clientY;

    cropper.pan(dx, dy);
  };

  const pointerUp = (event) => {
    dragging = false;

    cropper.canvas.releasePointerCapture(event.pointerId);
  };

  cropper.canvas.addEventListener("pointerdown", pointerDown);

  cropper.canvas.addEventListener("pointermove", pointerMove);

  cropper.canvas.addEventListener("pointerup", pointerUp);

  addCleanup(() => {
    cropper.canvas.removeEventListener("pointerdown", pointerDown);

    cropper.canvas.removeEventListener("pointermove", pointerMove);

    cropper.canvas.removeEventListener("pointerup", pointerUp);
  });
}

function resetSliders() {
  zoomSlider.value = 1;

  brightnessSlider.value = 100;

  contrastSlider.value = 100;

  saturationSlider.value = 100;
}

export async function openCropModal({
  imageFile,

  aspectRatio = 1,

  onSave,
}) {
  modal = document.getElementById("crop-modal");
  if (!modal) {
    throw new Error("#crop-modal not found.");
  }

  previewContainer = qs(".crop-preview");

  saveButton = qs(".crop-save");

  cancelButton = qs(".crop-cancel");

  resetButton = qs(".crop-reset");

  zoomSlider = qs(".crop-zoom");

  brightnessSlider = qs(".crop-brightness");

  contrastSlider = qs(".crop-contrast");

  saturationSlider = qs(".crop-saturation");

  rotateLeftButton = qs(".crop-rotate-left");

  rotateRightButton = qs(".crop-rotate-right");

  flipHorizontalButton = qs(".crop-flip-horizontal");

  flipVerticalButton = qs(".crop-flip-vertical");

  cropper = await createCropper(
    imageFile,

    aspectRatio,
  );

  updateCanvas();

  document.addEventListener(
    "keydown",

    escHandler,
  );

  addCleanup(() => document.removeEventListener("keydown", escHandler));

  modal.addEventListener(
    "click",

    outsideClickHandler,
  );

  addCleanup(() => modal.removeEventListener("click", outsideClickHandler));

  bindSlider(
    zoomSlider,

    (value) => {
      cropper.zoom(Number(value));
    },
  );

  bindSlider(
    brightnessSlider,

    (value) => {
      cropper.setBrightness(Number(value));
    },
  );

  bindSlider(
    contrastSlider,

    (value) => {
      cropper.setContrast(Number(value));
    },
  );

  bindSlider(
    saturationSlider,

    (value) => {
      cropper.setSaturation(Number(value));
    },
  );

  bindButton(
    rotateLeftButton,

    () => {
      cropper.rotate(-90);
    },
  );

  bindButton(
    rotateRightButton,

    () => {
      cropper.rotate(90);
    },
  );

  bindButton(
    flipHorizontalButton,

    () => {
      cropper.flipHorizontal();
    },
  );

  bindButton(
    flipVerticalButton,

    () => {
      cropper.flipVertical();
    },
  );
  bindButton(
    resetButton,

    () => {
      cropper.reset();

      resetSliders();
    },
  );

  bindButton(
    cancelButton,

    () => {
      closeModal();
    },
  );

  bindButton(
    saveButton,

    async () => {
      saveButton.disabled = true;

      try {
        const blob = await cropper.exportBlob();

        if (!blob) {
          throw new Error("Failed to export image.");
        }

        await onSave(blob);
        cropper.destroy();
        closeModal();
      } catch (error) {
        console.error(error);
      } finally {
        saveButton.disabled = false;
      }
    },
  );

  modal.classList.remove("hidden");

  modal.classList.add("show");

  modal.setAttribute("aria-hidden", "false");
}

/* ==========================================================
   Optional Public Helpers
========================================================== */

export function getCropper() {
  return cropper;
}

export function destroyCropper() {
  closeModal();
}

export async function replaceImage(file) {
  if (!modal) return;

  const state = cropper?.getState();

  cropper = await createCropper(file, cropper?.settings?.aspectRatio ?? 1);

  if (state) {
    cropper.setState(state);
  }

  updateCanvas();
}

export function resetCropper() {
  if (!cropper) return;

  cropper.reset();

  cropper.render();

  resetSliders();
}

export function rotateLeft() {
  cropper?.rotate(-90);
}

export function rotateRight() {
  cropper?.rotate(90);
}

export function flipHorizontal() {
  cropper?.flipHorizontal();
}

export function flipVertical() {
  cropper?.flipVertical();
}

export function setZoom(value) {
  cropper?.zoom(value);
}

export function setBrightness(value) {
  cropper?.setBrightness(value);
}

export function setContrast(value) {
  cropper?.setContrast(value);
}

export function setSaturation(value) {
  cropper?.setSaturation(value);
}

export async function exportBlob() {
  if (!cropper) {
    return null;
  }

  return await cropper.exportBlob();
}

export function exportDataURL() {
  if (!cropper) {
    return "";
  }

  return cropper.exportDataURL();
}
