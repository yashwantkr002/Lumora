from .base import *
DEBUG = False


ALLOWED_HOSTS = env.list(
    'DJANGO_ALLOWED_HOSTS',
    default=['127.0.0.1', 'localhost']
)

if DEBUG:
    INSTALLED_APPS += ["django_browser_reload"]
    MIDDLEWARE +=  ["django_browser_reload.middleware.BrowserReloadMiddleware"]