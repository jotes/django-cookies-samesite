# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import


DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!_sr1vb(h8l4+%vmizl#*9kc04&56v^!73(vo&fe&a2r_o!+h_'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = [
    'django.contrib.sessions',
]

MIDDLEWARE = [
    'django_cookies_samesite.middleware.CookiesSameSite',
    'django.contrib.sessions.middleware.SessionMiddleware',
]

SITE_ID = 1
