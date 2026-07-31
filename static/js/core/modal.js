/*
===========================================================
File: static/js/core/modal.js
===========================================================

Purpose

Reusable Modal Engine

Used By

✓ Login
✓ Register
✓ Forgot Password
✓ Edit Profile
✓ Avatar Cropper
✓ Cover Cropper
✓ Delete Confirmation
✓ Image Preview
✓ Settings

===========================================================
*/

"use strict";

/* ---------------------------------------------------------
 * Imports
 * ------------------------------------------------------ */

import events from "./events.js";

import {
    isString,
    isHTMLElement,
} from "./utils.js";

/* ---------------------------------------------------------
 * Constants
 * ------------------------------------------------------ */

export const MODAL_STATUS = Object.freeze({

    CLOSED: "closed",

    OPENING: "opening",

    OPEN: "open",

    CLOSING: "closing",

});

export const DEFAULT_MODAL_OPTIONS = Object.freeze({

    closeOnEscape: true,

    closeOnBackdrop: true,

    lockScroll: true,

    restoreFocus: true,

    trapFocus: true,

    animationDuration: 300,

});

/* ---------------------------------------------------------
 * Error Classes
 * ------------------------------------------------------ */

export class ModalError extends Error {

    constructor(
        message,
        code = "MODAL_ERROR",
    ) {

        super(message);

        this.name = "ModalError";

        this.code = code;

    }

}

export class ModalNotFoundError extends ModalError {

    constructor(id) {

        super(

            `Modal "${id}" not found.`,

            "MODAL_NOT_FOUND",

        );

    }

}

export class InvalidModalError extends ModalError {

    constructor() {

        super(

            "Expected HTMLElement.",

            "INVALID_MODAL",

        );

    }

}

/* ---------------------------------------------------------
 * Validation
 * ------------------------------------------------------ */

function validateModalElement(element) {

    if (!isHTMLElement(element)) {

        throw new InvalidModalError();

    }

}

function validateModalId(id) {

    if (

        !isString(id) ||

        id.trim() === ""

    ) {

        throw new ModalError(

            "Invalid modal id.",

            "INVALID_MODAL_ID",

        );

    }

}

/* ---------------------------------------------------------
 * Modal Class
 * ------------------------------------------------------ */

export class Modal {

    /**
     * @param {string} id
     * @param {HTMLElement} element
     * @param {Object} options
     */
    constructor(

        id,

        element,

        options = {},

    ) {

        validateModalId(id);

        validateModalElement(element);

        this.id = id;

        this.element = element;

        this.options = {

            ...DEFAULT_MODAL_OPTIONS,

            ...options,

        };

        this.status =
            MODAL_STATUS.CLOSED;

        this.previousFocus =
            null;

    }

    /**
     * Is modal open?
     *
     * @returns {boolean}
     */
    isOpen() {

        return (

            this.status ===

            MODAL_STATUS.OPEN

        );

    }

    /**
     * Open modal.
     *
     * @returns {Modal}
     */
    open() {

        if (this.isOpen()) {

            return this;

        }

        this.previousFocus = document.activeElement;

        this.status = MODAL_STATUS.OPENING;

        this.element.hidden = false;

        const firstFocusable =

            this.element.querySelector(

                'button, input, textarea, select, a, [tabindex]:not([tabindex="-1"])'

            );

        firstFocusable?.focus();

        this.element.setAttribute(
            "aria-hidden",
            "false",
        );

        this.element.classList.add(
            "is-open",
        );

        if (this.options.lockScroll) {

            modalManager.lockScroll();

        }

        modalManager.setActive(this);

        requestAnimationFrame(() => {

            this.status = MODAL_STATUS.OPEN;

        });

        events.emit(
            "modal:open",
            this,
        );

        return this;

    }

    /**
     * Close modal.
     *
     * @returns {Modal}
     */
    close() {

        if (!this.isOpen()) {

            return this;

        }

        this.status = MODAL_STATUS.CLOSING;

        this.element.classList.remove(
            "is-open",
        );

        this.element.hidden = true;

        this.element.setAttribute(
            "aria-hidden",
            "true",
        );

        if (this.options.lockScroll) {

            modalManager.unlockScroll();

        }

        if (

            this.options.restoreFocus &&

            this.previousFocus instanceof HTMLElement

        ) {

            this.previousFocus.focus();

        }

        modalManager.clearActive();

        requestAnimationFrame(() => {

            this.status = MODAL_STATUS.CLOSED;

        });

        events.emit(
            "modal:close",
            this,
        );

        return this;

    }

    /**
     * Toggle modal.
     *
     * @returns {Modal}
     */
    toggle() {

        if (this.isOpen()) {

            return this.close();

        }

        return this.open();

    }

    /**
     * Keep keyboard focus inside modal.
     */
    trapFocus(event) {

        if (

            !this.options.trapFocus ||

            event.key !== "Tab"

        ) {

            return;

        }

        const focusable = this.element.querySelectorAll(

            'button, a, input, textarea, select, [tabindex]:not([tabindex="-1"])'

        );

        if (!focusable.length) {

            return;

        }

        const first = focusable[0];

        const last = focusable[focusable.length - 1];

        if (

            event.shiftKey &&

            document.activeElement === first

        ) {

            event.preventDefault();

            last.focus();

        }

        else if (

            !event.shiftKey &&

            document.activeElement === last

        ) {

            event.preventDefault();

            first.focus();

        }

    }

    /**
     * Bind modal events.
     *
     * @returns {Modal}
     */
    bind() {

        this.handleKeyDown = (event) => {

            this.trapFocus(event);

            if (
                event.key === "Escape" &&
                this.options.closeOnEscape &&
                this.isOpen()
            ) {

                this.close();

            }

        };

        this.handleBackdropClick = (event) => {

            if (
                this.options.closeOnBackdrop &&
                event.target === this.element
            ) {

                this.close();

            }

        };

        document.addEventListener(
            "keydown",
            this.handleKeyDown,
        );

        this.element.addEventListener(
            "click",
            this.handleBackdropClick,
        );

        return this;

    }

    /**
     * Remove modal events.
     *
     * @returns {Modal}
     */
    unbind() {

        document.removeEventListener(
            "keydown",
            this.handleKeyDown,
        );

        this.element.removeEventListener(
            "click",
            this.handleBackdropClick,
        );

        return this;

    }

    /**
     * Initialize modal.
     *
     * @returns {Modal}
     */
    init() {

        this.bind();

        this.element.hidden = true;

        this.element.setAttribute(
            "aria-modal",
            "true",
        );

        const title = this.element.querySelector(

            'h1[id], h2[id], h3[id], h4[id], h5[id], h6[id]'

        );

        if (title && title.id) {

            this.element.setAttribute(

                "aria-labelledby",

                title.id,

            );

        }

        this.element.setAttribute(
            "aria-hidden",
            "true",
        );

        this.element.setAttribute(
            "role",
            "dialog",
        );

        this.element.setAttribute(
            "tabindex",
            "-1",
        );

        return this;

    }

    /**
     * Destroy modal.
     */
    destroy() {

        this.close();

        this.unbind();

        this.element.remove();

    }

    /**
     * Create modal from selector.
     *
     * @param {string} id
     * @param {string} selector
     * @param {Object} options
     *
     * @returns {Modal}
     */
    static fromSelector(

        id,

        selector,

        options = {},

    ) {

        const element =

            document.querySelector(selector);

        return new Modal(

            id,

            element,

            options,

        );

    }

}

/* ---------------------------------------------------------
 * Default Manager
 * ------------------------------------------------------ */
// Default manager will be exported after the class definition.
/* ---------------------------------------------------------
 * Modal Manager
 * ------------------------------------------------------ */

export class ModalManager {

    constructor() {

        this.activeModal = null;

        this.modals = new Map();

        this.stack = [];

        this.body = document.body;

    }

    /**
     * Open modal
     *
     * @param {Modal} modal
     */
    setActive(modal) {

        this.activeModal = modal;

    }

    /**
     * Clear active modal
     */
    clearActive() {

        this.activeModal = null;

    }

    /**
     * Get active modal
     *
     * @returns {Modal|null}
     */
    getActive() {

        return this.activeModal;

    }

    /**
     * Is any modal open?
     *
     * @returns {boolean}
     */
    hasActive() {

        return this.activeModal !== null;

    }

    /**
     * Lock body scroll
     */
    lockScroll() {

        this.body.style.overflow = "hidden";

    }

    /**
     * Unlock body scroll
     */
    unlockScroll() {

        this.body.style.overflow = "";

    }

    /* ---------------------------------------------------------
     * Modal Manager — additional methods
     * ------------------------------------------------------ */

    /**
     * Register modal.
     *
     * @param {Modal} modal
     *
     * @returns {Modal}
     */
    register(modal) {

        if (!(modal instanceof Modal)) {

            throw new ModalError(

                "Expected Modal instance.",

                "INVALID_MODAL",

            );

        }

        if (this.modals.has(modal.id)) {

            throw new ModalError(

                `Modal "${modal.id}" already registered.`,

                "MODAL_EXISTS",

            );

        }

        this.modals.set(

            modal.id,

            modal,

        );

        return modal;

    }

    /**
     * Unregister modal.
     *
     * @param {string} id
     */
    unregister(id) {

        validateModalId(id);

        this.stack = this.stack.filter(

            modalId => modalId !== id,

        );

        return this.modals.delete(id);

    }

    /**
     * Check modal exists.
     *
     * @param {string} id
     *
     * @returns {boolean}
     */
    hasModal(id) {

        validateModalId(id);

        return this.modals.has(id);

    }

    /**
     * Get modal.
     *
     * @param {string} id
     *
     * @returns {Modal}
     */
    getModal(id) {

        validateModalId(id);

        const modal = this.modals.get(id);

        if (!modal) {

            throw new ModalNotFoundError(id);

        }

        return modal;

    }

    /**
     * Get active modal.
     *
     * @returns {Modal|null}
     */
    getActiveModal() {

        if (this.stack.length === 0) {

            return null;

        }

        const id =

            this.stack[

                this.stack.length - 1

            ];

        return this.getModal(id);

    }

    /**
     * Push modal to stack.
     *
     * @param {string} id
     */
    push(id) {

        this.stack = this.stack.filter(

            modalId => modalId !== id,

        );

        this.stack.push(id);

    }

    /**
     * Remove modal from stack.
     *
     * @param {string} id
     */
    remove(id) {

        this.stack = this.stack.filter(

            modalId => modalId !== id,

        );

    }

    /**
     * Is modal active?
     *
     * @param {string} id
     *
     * @returns {boolean}
     */
    isActive(id) {

        const active =

            this.getActiveModal();

        return active?.id === id;

    }

    /**
     * Get stack size.
     *
     * @returns {number}
     */
    stackSize() {

        return this.stack.length;

    }

    /**
     * Get registered modal ids.
     *
     * @returns {string[]}
     */
    modalIds() {

        return [

            ...this.modals.keys(),

        ];

    }

}

export default new ModalManager();





