"""
ASGI config for Mvideos project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lumora.settings.development')
# for production, use the production settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lumora.settings.production')
application = get_asgi_application()
