import os
import sys

from django.utils.translation import gettext_lazy as _
from gt.common import TRUE_VALUES

TEST_MODE = False
if 'test' in sys.argv:
    # Detect automatically the test mode
    TEST_MODE = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(__file__)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')59c10'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG', False) in TRUE_VALUES else False

ALLOWED_HOSTS = ['*']
allowed_hosts_env = ''.join(os.environ.get(
    'ALLOWED_HOSTS', '*').split()).split(',')
if allowed_hosts_env and allowed_hosts_env != ['']:
    ALLOWED_HOSTS = allowed_hosts_env

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'baton',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'gt.vehicle',
    'gt.service',
    'baton.autodiscover',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

ROOT_URLCONF = 'gt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gt.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/sqlite3/gt.db',
    }
}


AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en-us', _('American English')),
    ('el', _('Greek')),
]
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

TIME_ZONE = 'Europe/Athens'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static'

LOG_LEVEL = 'DEBUG' if DEBUG is True else 'INFO'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'app_stream'
        },
    },
    'formatters': {
        'app_stream': {
            'format': '[%(asctime)s %(name)s %(levelname)s] %(message)s',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
    'loggers': {
    },
}

BATON = {
    'SITE_HEADER': 'GT Workshop',
    'SITE_TITLE': 'GT Workshop',
    'INDEX_TITLE': 'Site administration',
    'SUPPORT_HREF': '',
    'COPYRIGHT': 'copyright © 2021 Fotis Athinaios',
    'POWERED_BY': '',
    'CONFIRM_UNSAVED_CHANGES': True,
    'SHOW_MULTIPART_UPLOADING': True,
    'ENABLE_IMAGES_PREVIEW': True,
    'CHANGELIST_FILTERS_IN_MODAL': True,
    'CHANGELIST_FILTERS_ALWAYS_OPEN': False,
    'COLLAPSABLE_USER_AREA': False,
    'MENU_ALWAYS_COLLAPSED': True,
    'MENU_TITLE': 'Menu',
    'GRAVATAR_DEFAULT_IMG': 'retro',
}
