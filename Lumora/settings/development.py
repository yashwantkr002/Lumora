from .base import *

DEBUG = True

# In development, allow localhost and default local hosts
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Override any production-only settings if needed

# Add development-specific apps or middleware if required
