# Cookie library has moved to http in python3
try:
    import Cookie
except ImportError:
    import http.cookies as Cookie

import warnings

import django

from distutils.version import LooseVersion

from django.conf import settings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


Cookie.Morsel._reserved['samesite'] = 'SameSite'


class CookiesSameSite(MiddlewareMixin):
    """
    Support for SameSite attribute in Cookies is implemented in Django 2.1 and won't
    be backported to Django 1.11.x.
    This middleware will be obsolete when your app will start using Django 2.1.
    """
    def process_response(self, request, response):
        if LooseVersion(django.__version__) >= LooseVersion('2.1.0'):
            raise DeprecationWarning(
                'Your version of Django supports SameSite flag in the cookies mechanism. '
                'You should remove django-cookies-samesite from your project.'
            )

        protected_cookies = getattr(
            settings,
            'SESSION_COOKIE_SAMESITE_KEYS',
            set()
        ) or set()

        if not isinstance(protected_cookies, (list, set, tuple)):
            raise ValueError('SESSION_COOKIE_SAMESITE_KEYS should be a list, set or tuple.')

        protected_cookies = set(protected_cookies)
        protected_cookies |= {settings.SESSION_COOKIE_NAME, settings.CSRF_COOKIE_NAME}

        samesite_flag = getattr(
            settings,
            'SESSION_COOKIE_SAMESITE',
            None
        )

        if not samesite_flag:
            return response

        if samesite_flag.lower() not in {'lax', 'strict'}:
            raise ValueError('samesite must be "lax" or "strict".')

        for cookie in protected_cookies:
            if cookie in response.cookies:
                response.cookies[cookie]['samesite'] = samesite_flag.lower()

        return response
