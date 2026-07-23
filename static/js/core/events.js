/*
===========================================================
File: static/js/core/events.js
===========================================================

Purpose

Application-wide Event Bus

Used By

✓ Upload
✓ Modal
✓ Toast
✓ Profile
✓ Avatar
✓ Cover
✓ Chat
✓ Stories
✓ Notifications
✓ Settings

===========================================================
*/

"use strict";

/* ---------------------------------------------------------
 * Constants
 * ------------------------------------------------------ */

export const MAX_LISTENERS = 100;
export const WILDCARD_EVENT = "*";

/* ---------------------------------------------------------
 * Error Classes
 * ------------------------------------------------------ */

export class EventError extends Error {
  constructor(message, code = "EVENT_ERROR") {
    super(message);
    this.name = "EventError";
    this.code = code;
  }
}

export class InvalidEventNameError extends EventError {
  constructor(name) {
    super(`Invalid event name: ${String(name)}`, "INVALID_EVENT_NAME");
    this.name = "InvalidEventNameError";
  }
}

export class InvalidListenerError extends EventError {
  constructor() {
    super("Listener must be a function.", "INVALID_LISTENER");
    this.name = "InvalidListenerError";
  }
}

/* ---------------------------------------------------------
 * Validation Helpers
 * ------------------------------------------------------ */

function validateEventName(event) {
  if (typeof event !== "string" || event.trim() === "") {
    throw new InvalidEventNameError(event);
  }
}

function validateListener(listener) {
  if (typeof listener !== "function") {
    throw new InvalidListenerError();
  }
}

/* ---------------------------------------------------------
 * EventEmitter
 * ------------------------------------------------------ */

export class EventEmitter {
  constructor() {
    this.listeners = new Map();
  }

  getListeners(event) {
    validateEventName(event);

    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }

    return this.listeners.get(event);
  }

  on(event, listener) {
    validateEventName(event);
    validateListener(listener);

    const listeners = this.getListeners(event);

    if (listeners.size >= MAX_LISTENERS) {
      throw new EventError(
        `Maximum listeners (${MAX_LISTENERS}) exceeded.`,
        "MAX_LISTENERS_EXCEEDED",
      );
    }

    listeners.add(listener);

    return this;
  }

  once(event, listener) {
    validateEventName(event);
    validateListener(listener);

    const wrapper = (...args) => {
      this.off(event, wrapper);
      listener(...args);
    };

    return this.on(event, wrapper);
  }

  off(event, listener) {
    validateEventName(event);
    validateListener(listener);

    const listeners = this.listeners.get(event);

    if (!listeners) {
      return this;
    }

    listeners.delete(listener);

    if (listeners.size === 0) {
      this.listeners.delete(event);
    }

    return this;
  }

  has(event, listener) {
    validateEventName(event);
    validateListener(listener);

    const listeners = this.listeners.get(event);

    if (!listeners) {
      return false;
    }

    return listeners.has(listener);
  }

  listenerCount(event) {
    validateEventName(event);

    const listeners = this.listeners.get(event);

    return listeners ? listeners.size : 0;
  }

  getMatchingListeners(event) {
    const listeners = new Set();

    const exact = this.listeners.get(event);
    if (exact) {
      exact.forEach((listener) => listeners.add(listener));
    }

    const separator = event.indexOf(":");
    if (separator !== -1) {
      const namespace = event.substring(0, separator);
      const wildcard = `${namespace}:*`;
      const namespaceListeners = this.listeners.get(wildcard);

      if (namespaceListeners) {
        namespaceListeners.forEach((listener) => listeners.add(listener));
      }
    }

    const globalListeners = this.listeners.get(WILDCARD_EVENT);
    if (globalListeners) {
      globalListeners.forEach((listener) => listeners.add(listener));
    }

    return listeners;
  }

  emit(event, payload = null) {
    validateEventName(event);

    const listeners = this.getMatchingListeners(event);
    if (listeners.size === 0) {
      return false;
    }

    for (const listener of listeners) {
      try {
        listener(payload, event, this);
      } catch (error) {
        console.error(`[Event Error] ${event}`, error);
      }
    }

    return true;
  }

  async emitAsync(event, payload = null) {
    validateEventName(event);

    const listeners = this.getMatchingListeners(event);
    if (listeners.size === 0) {
      return false;
    }

    for (const listener of listeners) {
      try {
        await listener(payload, event, this);
      } catch (error) {
        console.error(`[Event Error] ${event}`, error);
      }
    }

    return true;
  }

  removeAllListeners(event = null) {
    if (event === null) {
      this.listeners.clear();
      return this;
    }

    validateEventName(event);
    this.listeners.delete(event);

    return this;
  }

  clear() {
    return this.removeAllListeners();
  }

  eventNames() {
    return [...this.listeners.keys()];
  }

  totalListenerCount() {
    let count = 0;

    for (const listeners of this.listeners.values()) {
      count += listeners.size;
    }

    return count;
  }

  destroy() {
    this.listeners.clear();
  }
}

/* ---------------------------------------------------------
 * Factory
 * ------------------------------------------------------ */

export function createEventBus() {
  return new EventEmitter();
}

/* ---------------------------------------------------------
 * Default Instance
 * ------------------------------------------------------ */

const events = createEventBus();

export default events;