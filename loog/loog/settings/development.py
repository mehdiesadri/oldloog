from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MEDIA_ROOT = BASE_DIR / 'media'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Django Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "chat.routing.channel_routing",
    },
}

# SMTP: For sending email to users
# https://docs.djangoproject.com/en/3.2/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

