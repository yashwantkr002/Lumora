/**
 * ===========================================================
 * Application Constants
 * ===========================================================
 */

export const HttpMethod = Object.freeze({

    GET: "GET",
    POST: "POST",
    PUT: "PUT",
    PATCH: "PATCH",
    DELETE: "DELETE",

});

export const Events = Object.freeze({

    POST_CREATED: "post:created",

    POST_UPDATED: "post:updated",

    POST_DELETED: "post:deleted",

    COMMENT_CREATED: "comment:created",

    COMMENT_DELETED: "comment:deleted",

    LIKE_CHANGED: "like:changed",

    SAVE_CHANGED: "save:changed",

    FOLLOW_CHANGED: "follow:changed",

    NOTIFICATION_RECEIVED: "notification:received",

});