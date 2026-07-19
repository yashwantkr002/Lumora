/**
 * ===========================================================
 * File: static/js/common/toast.js
 * ===========================================================
 *
 * PURPOSE
 *
 * Global toast notification service.
 *
 * ===========================================================
 */

class Toast {

    /**
     * -------------------------------------------------------
     * Success
     * -------------------------------------------------------
     */

    static success(message) {

        Toast.show(
            message,
            "success",
        );

    }

    /**
     * -------------------------------------------------------
     * Error
     * -------------------------------------------------------
     */

    static error(message) {

        Toast.show(
            message,
            "error",
        );

    }

    /**
     * -------------------------------------------------------
     * Info
     * -------------------------------------------------------
     */

    static info(message) {

        Toast.show(
            message,
            "info",
        );

    }

    /**
     * -------------------------------------------------------
     * Show Toast
     * -------------------------------------------------------
     */

    static show(
        message,
        type,
    ) {

        const container = document.getElementById(
            "toast-container",
        );

        if (!container) {

            return;

        }

        const toast =
            document.createElement(
                "div",
            );

        const colors = {

            success:
                "bg-green-600",

            error:
                "bg-red-600",

            info:
                "bg-blue-600",

        };

        toast.className = `
            pointer-events-auto
            rounded-xl
            px-5
            py-4
            text-white
            shadow-lg
            transition-all
            duration-300
            opacity-0
            translate-x-10
            ${colors[type]}
        `;

        toast.textContent =
            message;

        container.appendChild(
            toast,
        );

        requestAnimationFrame(
            () => {

                toast.classList.remove(
                    "opacity-0",
                    "translate-x-10",
                );

            },
        );

        setTimeout(
            () => {

                toast.classList.add(
                    "opacity-0",
                    "translate-x-10",
                );

                setTimeout(
                    () => {

                        toast.remove();

                    },
                    300,
                );

            },
            3000,
        );

    }

}

export default Toast;