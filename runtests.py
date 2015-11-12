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
        }
    },
    USE_TZ=True,
    ROOT_URLCONF='{0}.tests'.format(APP_NAME),
    #LOGGING = {
        #'version': 1,
        #'disable_existing_loggers': False,
        #'formatters': {
            #'simple': {
                #'format': '%(levelname)s %(message)s',
            #},
        #},
        #'handlers': {
            #'console': {
                #'level':'DEBUG',
                #'class':'logging.StreamHandler',
                #'formatter': 'simple',
                #'stream': sys.stdout,
            #},
        #},
        #'loggers': {
            #'impersonate': {
                #'handlers': ['console'],
                #'level': 'DEBUG',
                #'propagate': True,
            #},
        #},
    #},
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'impersonate.middleware.ImpersonateMiddleware',
    ),
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        APP_NAME,
    ),
    IMPERSONATE_DISABLE_LOGGING=True,
)

from django.test.utils import get_runner

django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests([APP_NAME])
if failures:
    sys.exit(failures)
