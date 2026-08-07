from pathlib import Path
import os
# from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent.parent
import environ
# load_dotenv()

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


SECRET_KEY = env('DJANGO_SECRET_KEY')
TAILWIND_APP_NAME = "theme"
import platform



if platform.system() == "Windows":
    NPM_BIN_PATH = "npm.cmd"
else:
    NPM_BIN_PATH = "/usr/local/bin/npm"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
]

EXTERNAL_APPS = [
    'app',
    "tailwind",
    "theme",
    'django.contrib.sites',
    'allauth',
    'cloudinary',
    'cloudinary_storage',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
]

INSTALLED_APPS += EXTERNAL_APPS


AUTH_USER_MODEL = 'app.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


ROOT_URLCONF = 'Lumora.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.unread_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'Lumora.wsgi.application'

DATABASES = {
    'default': env.db()
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_STORAGE_PROVIDER = "cloudinary"

MEDIA_UPLOAD_PATHS = {
    "avatars": "uploads/profile/avatars",
    "covers": "uploads/profile/covers",
    "posts": "uploads/posts",
    "stories": "uploads/stories",
    "videos": "uploads/videos",
}

# 
# -------------------------------------------------------
# Media Validation
# -------------------------------------------------------

MEDIA_UPLOAD_FOLDERS = {
    "avatars",
    "covers",
    "posts",
    "stories",
    "reels",
}

MEDIA_MAX_IMAGE_SIZE = 10 * 1024 * 1024

MEDIA_MAX_VIDEO_SIZE = 200 * 1024 * 1024


# 

STORAGES = {
    'default': {
        'BACKEND': (
            'app.core.storage.cloudinary.CloudinaryStorage'
            if env('CLOUDINARY_CLOUD_NAME') and env('CLOUDINARY_API_KEY') and env('CLOUDINARY_API_SECRET')
            else 'django.core.files.storage.FileSystemStorage'
        )
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    # तुम्हारा कस्टम ईमेल बैकएंड (सबसे पहले रन होगा)
    "app.authentication.email_backend.EmailBackend",
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_PASSWORD_MIN_LENGTH = 8
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[]
)

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

