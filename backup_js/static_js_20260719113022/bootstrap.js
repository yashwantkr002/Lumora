/**
 * ===========================================================
 * Application Bootstrap
 * ===========================================================
 */

import { AppConfig } from "./core/config.js";

console.info(

    `%c${AppConfig.APP_NAME} v${AppConfig.VERSION}`,

    "color:#6366f1;font-weight:bold;font-size:14px;"

);

document.dispatchEvent(

    new Event("lumora:ready")

);