# coding: utf-8

import os

PROJECT_ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT_PATH, 'db.sqlite3'),
    }
}
