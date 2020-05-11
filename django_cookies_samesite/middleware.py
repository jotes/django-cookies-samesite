# Cookie library has moved to http in python3
try:
    import Cookie
except ImportError:
    import http.cookies as Cookie

import django

from distutils.version import LooseVersion

from django.conf import settings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from django_cookies_samesite.user_agent_checker import UserAgentChecker

Cookie.Morsel._reserved['samesite'] = 'SameSite'
Cookie.Morsel._reserved.update({"samesite": "SameSite", "secure": 'Secure'})

# TODO: change this to 3.1.0 once Django 3.1 is released
DJANGO_SUPPORTED_VERSION = '3.0.0'


def get_config_setting(setting_name, default_value=None):
    """Load the Django setting with DCS_ prefix and fallback to the legacy name if not found."""
    return getattr(
        settings,
        "DCS_{}".format(setting_name),
        getattr(settings, setting_name, default_value)
    )


class CookiesSameSite(MiddlewareMixin):
    """
    Support for SameSite attribute in Cookies is fully implemented in Django 3.1 and won't
    be back-ported to Django 2.x.
    This middleware will be obsolete when your app will start using Django 3.1.
    """

    def __init__(self, *args, **kwargs):
        self.protected_cookies = get_config_setting("SESSION_COOKIE_SAMESITE_KEYS", set())

        if not isinstance(self.protected_cookies, (list, set, tuple)):
            raise ValueError("SESSION_COOKIE_SAMESITE_KEYS should be a list, set or tuple.")

        self.protected_cookies = set(self.protected_cookies)
        self.protected_cookies |= {settings.SESSION_COOKIE_NAME, settings.CSRF_COOKIE_NAME}

        samesite_flag = get_config_setting("SESSION_COOKIE_SAMESITE", "")
        self.samesite_flag = str(samesite_flag).capitalize() if samesite_flag is not None else ''
        self.samesite_force_all = get_config_setting("SESSION_COOKIE_SAMESITE_FORCE_ALL")

        return super(CookiesSameSite, self).__init__(*args, **kwargs)

    def update_cookie(self, cookie, request, response):
        response.cookies[cookie]['samesite'] = self.samesite_flag
        if request.is_secure():
            response.cookies[cookie]['secure'] = True

    def process_response(self, request, response):
        # same-site = None introduced for Chrome 80 breaks for Chrome 51-66
        # Refer (https://www.chromium.org/updates/same-site/incompatible-clients)
        http_user_agent = request.META.get('HTTP_USER_AGENT') or " "
        user_agent_checker = UserAgentChecker(http_user_agent)

        if user_agent_checker.do_not_send_same_site_policy:
            return response

        if LooseVersion(django.get_version()) >= LooseVersion(DJANGO_SUPPORTED_VERSION):
            raise DeprecationWarning(
                "Your version of Django supports SameSite flag in the cookies mechanism. "
                "You should remove django-cookies-samesite from your project."
            )

        if not self.samesite_flag:
            return response

        # TODO: capitalize those values
        if self.samesite_flag not in {'Lax', 'None', 'Strict'}:
            raise ValueError("samesite must be \"Lax\", \"None\", or \"Strict\".")

        if self.samesite_force_all:
            for cookie in response.cookies:
                self.update_cookie(cookie, request, response)
        else:
            for cookie in self.protected_cookies:
                if cookie in response.cookies:
                    self.update_cookie(cookie, request, response)

        return response
