#!/usr/bin/python
# -*- coding: utf-8 -*-

# Django settings for event_horizon project.

import os

PROJECT_ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Johann Vivot', 'Johann.Vivot@wmccann.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {},
    }
}

ALLOWED_HOSTS = []

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = False

MEDIA_ROOT = os.path.join(PROJECT_ROOT_PATH, 'public', 'media')
MEDIA_URL = '/public/media/'

STATIC_ROOT = '/public/'
STATIC_URL = '/public/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT_PATH, 'public'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'v7ge&a9+hi5+ld#j9+7xs^smk0nqn!u6lx&ali!=b4&uxj!o3t'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'event_horizon.urls'

WSGI_APPLICATION = 'event_horizon.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admin',

    # APPS

    'core',
    'metrics_social',
    'services_social',
    'social',
    'dashboard',
    'metrics_media',
    'services_media',
    'media',

    'south',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from development_config import *
except ImportError:
    pass

try:
    from production_config import *
except ImportError:
    pass


FACEBOOK_INSIGHTS_DAILY_METRICS = []
FACEBOOK_INSIGHTS_WEEKLY_METRICS = []
FACEBOOK_INSIGHTS_DAYS_28_METRICS = []
FACEBOOK_INSIGHTS_POSTS_METRICS = []
