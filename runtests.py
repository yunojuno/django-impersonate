# -*- coding: utf-8 -*-
import sys

import django
from django.conf import settings


APP_NAME = 'impersonate'

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        },
    },
    USE_TZ=True,
    ROOT_URLCONF='{0}.tests'.format(APP_NAME),
    # LOGGING = {
        # 'version': 1,
        # 'disable_existing_loggers': False,
        # 'formatters': {
            # 'simple': {
                # 'format': '%(levelname)s %(message)s',
            # },
        # },
        # 'handlers': {
            # 'console': {
                # 'level':'DEBUG',
                # 'class':'logging.StreamHandler',
                # 'formatter': 'simple',
                # 'stream': sys.stdout,
            # },
        # },
        # 'loggers': {
            # 'impersonate': {
                # 'handlers': ['console'],
                # 'level': 'DEBUG',
                # 'propagate': True,
            # },
        # },
    # },
    # Both MIDDLEWARE and MIDDLEWARE_CLASSES for testing purposes.
    MIDDLEWARE=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'impersonate.middleware.ImpersonateMiddleware',
    ),
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'impersonate.middleware.ImpersonateMiddleware',
    ),
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
    ],
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        APP_NAME,
    ),
    IMPERSONATE={'DISABLE_LOGGING': True},
)

from django.test.utils import get_runner

django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests([APP_NAME])
if failures:
    sys.exit(failures)
