/*
===========================================================
File: static/js/core/storage.js
===========================================================

Purpose

Reusable Storage Engine

Used By

✓ Authentication
✓ User Settings
✓ Theme
✓ Draft Posts
✓ Search History
✓ Cache
✓ Preferences
✓ Remember Me

===========================================================
*/

"use strict";

/* ---------------------------------------------------------
 * Imports
 * ------------------------------------------------------ */

import { isString } from "./utils.js";

/* ---------------------------------------------------------
 * Constants
 * ------------------------------------------------------ */

export const STORAGE_TYPES = Object.freeze({

    LOCAL: "local",

    SESSION: "session",

});

export const DEFAULT_STORAGE_OPTIONS = Object.freeze({

    namespace: "lumora",

    storage: STORAGE_TYPES.LOCAL,

    serialize: true,

});

/* ---------------------------------------------------------
 * Error Classes
 * ------------------------------------------------------ */

export class StorageError extends Error {

    constructor(

        message,

        code = "STORAGE_ERROR",

    ) {

        super(message);

        this.name = "StorageError";

        this.code = code;

    }

}

export class InvalidStorageKeyError extends StorageError {

    constructor() {

        super(

            "Storage key must be a non-empty string.",

            "INVALID_STORAGE_KEY",

        );

    }

}

export class StorageUnavailableError extends StorageError {

    constructor(type) {

        super(

            `${type} storage is unavailable.`,

            "STORAGE_UNAVAILABLE",

        );

    }

}

/* ---------------------------------------------------------
 * Validation
 * ------------------------------------------------------ */

function validateKey(key) {

    if (

        !isString(key) ||

        key.trim() === ""

    ) {

        throw new InvalidStorageKeyError();

    }

}

/* ---------------------------------------------------------
 * Storage Class
 * ------------------------------------------------------ */

export class Storage {

    /**
     * @param {Object} options
     */
    constructor(

        options = {},

    ) {

        this.options = {

            ...DEFAULT_STORAGE_OPTIONS,

            ...options,

        };

    }

    /**
     * Get namespace key.
     *
     * @param {string} key
     *
     * @returns {string}
     */
    getKey(key) {

        validateKey(key);

        return `${

            this.options.namespace

        }:${key}`;

    }
        /**
     * Get storage instance.
     *
     * @param {Object} options
     *
     * @returns {Storage}
     */
    getStorage(options = {}) {

        const type =

            options.storage ??

            this.options.storage;

        try {

            switch (type) {

                case STORAGE_TYPES.LOCAL:

                    window.localStorage.setItem(

                        "__storage_test__",

                        "1",

                    );

                    window.localStorage.removeItem(

                        "__storage_test__",

                    );

                    return window.localStorage;

                case STORAGE_TYPES.SESSION:

                    window.sessionStorage.setItem(

                        "__storage_test__",

                        "1",

                    );

                    window.sessionStorage.removeItem(

                        "__storage_test__",

                    );

                    return window.sessionStorage;

                default:

                    throw new StorageUnavailableError(

                        type,

                    );

            }

        }

        catch {

            throw new StorageUnavailableError(

                type,

            );

        }

    }

    /**
     * Store value.
     *
     * @param {string} key
     * @param {*} value
     * @param {Object} options
     *
     * @returns {Storage}
     */
    set(

        key,

        value,

        options = {},

    ) {

        validateKey(key);

        const storage =

            this.getStorage(options);

        const storageKey =

            this.getKey(key);

        const serialize =

            options.serialize ??

            this.options.serialize;

        const data =

            serialize

                ? JSON.stringify(value)

                : value;

        storage.setItem(

            storageKey,

            data,

        );


        return this;

    }

    /**
     * Get value.
     *
     * @param {string} key
     * @param {*} defaultValue
     * @param {Object} options
     *
     * @returns {*}
     */
    get(

        key,

        defaultValue = null,

        options = {},

    ) {

        validateKey(key);

        const storage =

            this.getStorage(options);

        const storageKey =

            this.getKey(key);

        const value =

            storage.getItem(storageKey);

        if (

            value === null

        ) {

            return defaultValue;

        }

        const serialize =

            options.serialize ??

            this.options.serialize;

        if (

            serialize

        ) {

            try {

                return JSON.parse(value);

            }

            catch {

                return defaultValue;

            }

        }

        return value;

    }

    /**
     * Remove value.
     *
     * @param {string} key
     * @param {Object} options
     *
     * @returns {Storage}
     */
    remove(

        key,

        options = {},

    ) {

        validateKey(key);

        const storage =

            this.getStorage(options);

        storage.removeItem(

            this.getKey(key),

        );

        return this;

    }

    /**
     * Check value exists.
     *
     * @param {string} key
     * @param {Object} options
     *
     * @returns {boolean}
     */
    has(

        key,

        options = {},

    ) {

        validateKey(key);

        const storage =

            this.getStorage(options);

        return (

            storage.getItem(

                this.getKey(key),

            ) !== null

        );

    }
        /**
     * Clear all namespaced values.
     *
     * @param {Object} options
     *
     * @returns {Storage}
     */
    clear(options = {}) {

        const storage =
            this.getStorage(options);

        const prefix =
            `${this.options.namespace}:`;

        const keys = [];

        for (

            let index = 0;

            index < storage.length;

            index++

        ) {

            const key =
                storage.key(index);

            if (

                key?.startsWith(prefix)

            ) {

                keys.push(key);

            }

        }

        keys.forEach(key => {

            storage.removeItem(key);

        });

        return this;

    }

    /**
     * Get all keys.
     *
     * @param {Object} options
     *
     * @returns {string[]}
     */
    keys(options = {}) {

        const storage =
            this.getStorage(options);

        const prefix =
            `${this.options.namespace}:`;

        const keys = [];

        for (

            let index = 0;

            index < storage.length;

            index++

        ) {

            const key =
                storage.key(index);

            if (

                key?.startsWith(prefix)

            ) {

                keys.push(

                    key.substring(

                        prefix.length,

                    ),

                );

            }

        }

        return keys;

    }

    /**
     * Get all values.
     *
     * @param {Object} options
     *
     * @returns {Array}
     */
    values(options = {}) {

        return this.keys(options).map(

            key =>

                this.get(

                    key,

                    null,

                    options,

                ),

        );

    }

    /**
     * Get all entries.
     *
     * @param {Object} options
     *
     * @returns {Array}
     */
    entries(options = {}) {

        return this.keys(options).map(

            key => [

                key,

                this.get(

                    key,

                    null,

                    options,

                ),

            ],

        );

    }

    /**
     * Storage size.
     *
     * @param {Object} options
     *
     * @returns {number}
     */
    size(options = {}) {

        return this.keys(

            options,

        ).length;

    }
        /**
     * Store value with expiry.
     *
     * @param {string} key
     * @param {*} value
     * @param {number} ttl
     * @param {Object} options
     *
     * @returns {Storage}
     */
    setWithExpiry(

        key,

        value,

        ttl,

        options = {},

    ) {

        const data = {

            value,

            expiresAt:

                Date.now() + ttl,

        };

        return this.set(

            key,

            data,

            options,

        );

    }

    /**
     * Get value with expiry.
     *
     * @param {string} key
     * @param {*} defaultValue
     * @param {Object} options
     *
     * @returns {*}
     */
    getWithExpiry(

        key,

        defaultValue = null,

        options = {},

    ) {

        const data = this.get(

            key,

            null,

            options,

        );

        if (

            !data ||

            typeof data !== "object"

        ) {

            return defaultValue;

        }

        if (

            Date.now() >

            data.expiresAt

        ) {

            this.remove(

                key,

                options,

            );

            return defaultValue;

        }

        return data.value;

    }

    /**
     * Check whether a key has expired.
     *
     * @param {string} key
     * @param {Object} options
     *
     * @returns {boolean}
     */
    isExpired(

        key,

        options = {},

    ) {

        const data = this.get(

            key,

            null,

            options,

        );

        if (

            !data ||

            typeof data !== "object"

        ) {

            return true;

        }

        return (

            Date.now() >

            data.expiresAt

        );

    }

    /**
     * Remove all expired items.
     *
     * @param {Object} options
     *
     * @returns {Storage}
     */
    clearExpired(

        options = {},

    ) {

        this.keys(options).forEach(

            key => {

                this.getWithExpiry(

                    key,

                    null,

                    options,

                );

            },

        );

        return this;

    }

    /**
     * Destroy storage.
     *
     * @returns {Storage}
     */
    destroy() {

        this.clear();

        return this;

    }

}

/* ---------------------------------------------------------
 * Default Instance
 * ------------------------------------------------------ */

export const storage =

    new Storage();

export default storage;