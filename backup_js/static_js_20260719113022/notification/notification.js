/*
===========================================================
File: static/js/notification/notification.js
===========================================================

PURPOSE

Notification interactions.

- Mark notification as read
- Mark all notifications as read
- Clear read notifications

===========================================================
*/

import Ajax from "../core/ajax.js";
import Toast from "../common/toast.js";

class NotificationManager {

    constructor() {

        this.initialize();

    }

    initialize() {

        this.bindMarkRead();

        this.bindMarkAllRead();

        this.bindClearRead();

    }

    bindMarkRead() {

        document.addEventListener("click", async (event) => {

            const button = event.target.closest(
                "[data-notification-read]"
            );

            if (!button) return;

            event.preventDefault();

            try {

                const response = await Ajax.post(
                    button.dataset.url,
                );

                if (response.success) {

                    button
                        .closest("[data-notification-card]")
                        ?.classList.remove(
                            "border-l-primary"
                        );

                    button.remove();

                    Toast.success(
                        "Notification marked as read."
                    );

                }

            } catch {

                Toast.error(
                    "Unable to update notification."
                );

            }

        });

    }

    bindMarkAllRead() {

        document.addEventListener("submit", async (event) => {

            const form = event.target;

            if (!form.matches("[data-mark-all-read]")) {

                return;

            }

            event.preventDefault();

            try {

                const response = await Ajax.post(
                    form.action,
                );

                if (response.success) {

                    location.reload();

                }

            } catch {

                Toast.error(
                    "Unable to mark notifications."
                );

            }

        });

    }

    bindClearRead() {

        document.addEventListener("submit", async (event) => {

            const form = event.target;

            if (!form.matches("[data-clear-read]")) {

                return;

            }

            event.preventDefault();

            try {

                const response = await Ajax.post(
                    form.action,
                );

                if (response.success) {

                    location.reload();

                }

            } catch {

                Toast.error(
                    "Unable to clear notifications."
                );

            }

        });

    }

}

new NotificationManager();