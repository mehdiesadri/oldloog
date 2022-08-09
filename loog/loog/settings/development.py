from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
CELERY_ENABLED = False

MEDIA_ROOT = BASE_DIR / 'media'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# SMTP: For sending email to users
# https://docs.djangoproject.com/en/3.2/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
