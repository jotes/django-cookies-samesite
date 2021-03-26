# -*- encoding: utf-8 -*-
import unittest
from contextlib import contextmanager
from distutils.version import LooseVersion

from mock import patch

import django

from ddt import ddt, data
from django.test import TestCase

from django_cookies_samesite.middleware import DJANGO_SUPPORTED_VERSION, CookiesSameSite


@ddt
class CookieSamesiteConfigTests(TestCase):
    def test_settings_default_values(self):
        """Check if middleware reads default values as expected"""
        with self.settings():
            middleware = CookiesSameSite()
            self.assertEqual(middleware.samesite_force_all, None)
            self.assertEqual(middleware.protected_cookies, {'sessionid', 'csrftoken'})

            if LooseVersion(django.get_version()) >= LooseVersion('3.0'):
                self.assertEqual(middleware.samesite_flag, 'Lax')
            else:
                self.assertEqual(middleware.samesite_flag, '')

    @data(
        '',
        'DCS_'
    )
    def test_settings(self, config_prefix):
        """
        Check if the cookie middleware fetches prefixed settings.
        """
        with self.settings(**{
            "{}SESSION_COOKIE_SAMESITE".format(config_prefix): 'Lax',
            "{}SESSION_COOKIE_SAMESITE_FORCE_ALL".format(config_prefix): True,
            "{}SESSION_COOKIE_SAMESITE_KEYS".format(config_prefix): {'custom_cookie'},
        }):
            middleware = CookiesSameSite()
            self.assertEqual(middleware.samesite_flag, 'Lax')
            self.assertEqual(middleware.samesite_force_all, True)
            self.assertEqual(middleware.protected_cookies, {'sessionid', 'csrftoken', 'custom_cookie'})
    
        with(self.settings(**{
            "{}SESSION_COOKIE_SAMESITE_FORCE_CORE".format(config_prefix): False,
            "{}SESSION_COOKIE_SAMESITE_KEYS".format(config_prefix): {'custom_cookie'},
        })):
            middleware = CookiesSameSite()
            self.assertEqual(middleware.protected_cookies, {'custom_cookie'})


@ddt
class CookiesSamesiteTestsWithConfigPrefix(TestCase):
    config_prefix = "DCS_"

    @contextmanager
    def settings(self, **config_settings):
        """Override all settings with the prefix name"""

        def format_key(k):
            """Prefix only the middleware settings."""
            return "{}{}".format(self.config_prefix, k) if k.startswith("SESSION_COOKIE_SAMESITE") else k

        prefixed_settings = {
            format_key(k): v for k, v in config_settings.items()
        }
        with super(CookiesSamesiteTestsWithConfigPrefix, self).settings(**prefixed_settings):
            yield

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_samesite_Strict(self):
        with self.settings(SESSION_COOKIE_SAMESITE='Strict'):
            response = self.client.get('/cookies-test/')
            self.assertEqual(response.cookies['sessionid']['samesite'], 'Strict')
            self.assertEqual(response.cookies['csrftoken']['samesite'], 'Strict')

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('csrftoken=', cookies_string[0])
            self.assertTrue('; SameSite=Strict', cookies_string[0])
            self.assertTrue('sessionid=', cookies_string[2])
            self.assertTrue('; SameSite=Strict', cookies_string[2])

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_samesite_Lax(self):
        with self.settings(SESSION_COOKIE_SAMESITE='Lax'):
            response = self.client.get('/cookies-test/')
            self.assertEqual(response.cookies['sessionid']['samesite'], 'Lax')
            self.assertEqual(response.cookies['csrftoken']['samesite'], 'Lax')

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('csrftoken=' in cookies_string[0])
            self.assertTrue('; SameSite=Lax' in cookies_string[0])
            self.assertTrue('sessionid=' in cookies_string[2])
            self.assertTrue('; SameSite=Lax' in cookies_string[2])

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_samesite_none(self):
        with self.settings(SESSION_COOKIE_SAMESITE='None'):
            response = self.client.get('/cookies-test/')

            self.assertEqual(response.cookies['sessionid']['samesite'], 'None')
            self.assertEqual(response.cookies['csrftoken']['samesite'], 'None')

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('csrftoken=' in cookies_string[0])
            self.assertTrue('; SameSite=None' in cookies_string[0])
            self.assertTrue('sessionid=' in cookies_string[2])
            self.assertTrue('; SameSite=None' in cookies_string[2])

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_samesite_none_force_all(self):
        with self.settings(SESSION_COOKIE_SAMESITE='None', SESSION_COOKIE_SAMESITE_FORCE_ALL=True):
            response = self.client.get('/cookies-test/')
            self.assertEqual(response.cookies['sessionid']['samesite'], 'None')
            self.assertEqual(response.cookies['csrftoken']['samesite'], 'None')
            self.assertEqual(response.cookies['custom_cookie']['samesite'], 'None')
            self.assertEqual(response.cookies['zcustom_cookie']['samesite'], 'None')

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('custom_cookie=' in cookies_string[1])
            self.assertTrue('; SameSite=None' in cookies_string[1])
            self.assertTrue('csrftoken=' in cookies_string[0])
            self.assertTrue('; SameSite=None' in cookies_string[0])
            self.assertTrue('sessionid=' in cookies_string[2])
            self.assertTrue('; SameSite=None' in cookies_string[2])
            self.assertTrue('zcustom_cookie=' in cookies_string[3])
            self.assertTrue('; SameSite=None' in cookies_string[3])

    @unittest.skipIf(django.get_version() < DJANGO_SUPPORTED_VERSION, 'should skip if Django does not support')
    def test_cookie_samesite_django31(self):
        # Raise DeprecationWarning for newer versions of Django
        with patch('django.get_version', return_value=DJANGO_SUPPORTED_VERSION):
            with self.assertRaises(DeprecationWarning) as exc:
                self.client.get('/cookies-test/')

            self.assertEqual(exc.exception.args[0], (
                'Your version of Django supports SameSite flag in the cookies mechanism. '
                'You should remove django-cookies-samesite from your project.'
            ))

        with patch('django_cookies_samesite.middleware.django.get_version', return_value=DJANGO_SUPPORTED_VERSION):
            with self.assertRaises(DeprecationWarning) as exc:
                self.client.get('/cookies-test/')

            self.assertEqual(exc.exception.args[0], (
                'Your version of Django supports SameSite flag in the cookies mechanism. '
                'You should remove django-cookies-samesite from your project.'
            ))

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_samesite_custom_cookies(self):
        # Middleware shouldn't accept malformed settings
        with self.settings(
            SESSION_COOKIE_SAMESITE='Lax',
            SESSION_COOKIE_SAMESITE_KEYS='something'
        ):
            with self.assertRaises(ValueError) as exc:
                self.client.get('/cookies-test/')

            self.assertEqual(exc.exception.args[0], 'SESSION_COOKIE_SAMESITE_KEYS should be a list, set or tuple.')

        # Test if SameSite flags is set to custom cookies
        with self.settings(
            SESSION_COOKIE_SAMESITE='Lax',
            SESSION_COOKIE_SAMESITE_KEYS=('custom_cookie',)
        ):
            response = self.client.get('/cookies-test/')

            self.assertEqual(response.cookies['sessionid']['samesite'], 'Lax')
            self.assertEqual(response.cookies['csrftoken']['samesite'], 'Lax')
            self.assertEqual(response.cookies['custom_cookie']['samesite'], 'Lax')
            self.assertEqual(response.cookies['zcustom_cookie']['samesite'], '')

            cookies_string = sorted(response.cookies.output().split('\r\n'))

            self.assertTrue('custom_cookie=' in cookies_string[1])
            self.assertTrue('; SameSite=Lax' in cookies_string[1])
            self.assertTrue('csrftoken=' in cookies_string[0])
            self.assertTrue('; SameSite=Lax' in cookies_string[0])
            self.assertTrue('sessionid=' in cookies_string[2])
            self.assertTrue('; SameSite=Lax' in cookies_string[2])
            self.assertTrue('zcustom_cookie=' in cookies_string[3])
            self.assertTrue('; SameSite=Lax' not in cookies_string[3])

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_samesite_invalid(self):
        with self.settings(SESSION_COOKIE_SAMESITE='invalid'):
            with self.assertRaises(ValueError) as exc:
                self.client.get('/cookies-test/')

            self.assertEqual(exc.exception.args[0], 'samesite must be "Lax", "None", or "Strict".')

    @unittest.skipIf(django.get_version() >= '2.1.0', 'should skip if Django sets SameSite')
    def test_cookie_samesite_unset(self):
        with self.settings(SESSION_COOKIE_SAMESITE=None):
            response = self.client.get('/cookies-test/')
            self.assertEqual(response.cookies['sessionid'].get('samesite'), '')
            self.assertEqual(response.cookies['csrftoken'].get('samesite'), '')

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('csrftoken=' in cookies_string[0])
            self.assertTrue('; SameSite=Lax' not in cookies_string[0])
            self.assertTrue('; SameSite=Strict' not in cookies_string[0])
            self.assertTrue('; SameSite=None' not in cookies_string[0])
            self.assertTrue('sessionid=' in cookies_string[2])
            self.assertTrue('; SameSite=Lax' not in cookies_string[2])
            self.assertTrue('; SameSite=None' not in cookies_string[2])

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_names_changed(self):
        session_name = 'sessionid-test'
        csrf_name = 'csrftoken-test'
        with self.settings(
            SESSION_COOKIE_NAME=session_name,
            CSRF_COOKIE_NAME=csrf_name,
            SESSION_COOKIE_SAMESITE='Lax'
        ):
            response = self.client.get('/cookies-test/')

            self.assertEqual(response.cookies[session_name]['samesite'], 'Lax')
            self.assertEqual(response.cookies[csrf_name]['samesite'], 'Lax')
            cookies_string = sorted(response.cookies.output().split('\r\n'))

            self.assertTrue(csrf_name + '=' in cookies_string[0])
            self.assertTrue('; SameSite=Lax' in cookies_string[0])
            self.assertTrue(session_name + '=' in cookies_string[2])
            self.assertTrue('; SameSite=Lax' in cookies_string[2])

    @unittest.skipIf(django.get_version() >= '2.1.0', 'should skip if Django sets SameSite')
    @data(
        # Chrome
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    )
    def test_unsupported_browsers(self, ua_string):
        session_name = 'sessionid-test'
        csrf_name = 'csrftoken-test'

        with self.settings(
            SESSION_COOKIE_NAME=session_name,
            CSRF_COOKIE_NAME=csrf_name,
            SESSION_COOKIE_SAMESITE='Lax'
        ):
            response = self.client.get(
                '/cookies-test/',
                HTTP_USER_AGENT=ua_string,
            )
            self.assertEqual(response.cookies[session_name]['samesite'], '')
            self.assertEqual(response.cookies[csrf_name]['samesite'], '')

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('; SameSite=Lax' not in cookies_string[0])
            self.assertTrue('; SameSite=Lax' not in cookies_string[1])

    @data(
        # Chrome
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2704.103 Safari/537.36',
        # Firefox
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
        # Internet Explorer
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)",
        # Safari
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) "
        "Version/10.0 Mobile/14E304 Safari/602.1 "
    )
    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_supported_browsers(self, ua_string):
        session_name = 'sessionid-test'
        csrf_name = 'csrftoken-test'

        with self.settings(
            SESSION_COOKIE_NAME=session_name,
            CSRF_COOKIE_NAME=csrf_name,
            SESSION_COOKIE_SAMESITE='Lax'
        ):
            response = self.client.get(
                '/cookies-test/',
                HTTP_USER_AGENT=ua_string,
            )
            self.assertEqual(response.cookies[session_name]['samesite'], 'Lax')
            self.assertEqual(response.cookies[csrf_name]['samesite'], 'Lax')

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('; SameSite=Lax' in cookies_string[0])
            self.assertTrue('; SameSite=Lax' in cookies_string[2])

    @data(
        # Chrome
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2704.103 Safari/537.36",
        # Firefox
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
        # Internet Explorer
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)",
        # Safari
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) "
        "Version/10.0 Mobile/14E304 Safari/602.1 "
        # noqa
    )
    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_supported_browsers_with_secure_true(self, ua_string):
        session_name = 'sessionid-test'
        csrf_name = 'csrftoken-test'

        with self.settings(
            SESSION_COOKIE_NAME=session_name,
            CSRF_COOKIE_NAME=csrf_name,
            SESSION_COOKIE_SAMESITE='None'
        ):
            response = self.client.get(
                '/cookies-test/',
                HTTP_USER_AGENT=ua_string,
                secure=True,
            )
            self.assertEqual(response.cookies[session_name]['samesite'], 'None')
            self.assertEqual(response.cookies[session_name]['secure'], True)
            self.assertEqual(response.cookies[csrf_name]['samesite'], 'None')
            self.assertEqual(response.cookies[csrf_name]['secure'], True)

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('; SameSite=None; Secure' in cookies_string[0])
            self.assertTrue('; SameSite=None; Secure' in cookies_string[2])

    @data(
        b"Mozilla/5.0 (Linux; Android 7.1.2; Moto E\xef\xbf\xbd POWER) AppleWebKit/537.36",
        b"Mozilla/5.0 (Linux; Android 7.1.2; Moto E\xff\xff\xbd POWER) AppleWebKit/537.36",
    )
    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_user_agent_contains_non_ascii_characters(self, ua_string):
        """The middleware handles the case when an HTTP client's User Agent contains non-ascii characters."""
        session_name = 'sessionid-test'
        csrf_name = 'csrftoken-test'

        with self.settings(
            SESSION_COOKIE_NAME=session_name,
            CSRF_COOKIE_NAME=csrf_name,
            SESSION_COOKIE_SAMESITE='None'
        ):
            response = self.client.get(
                '/cookies-test/',
                HTTP_USER_AGENT=ua_string,
                secure=True,
            )
            self.assertEqual(response.cookies[session_name]['samesite'], 'None')
            self.assertEqual(response.cookies[session_name]['secure'], True)
            self.assertEqual(response.cookies[csrf_name]['samesite'], 'None')
            self.assertEqual(response.cookies[csrf_name]['secure'], True)

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('; SameSite=None; Secure' in cookies_string[0])
            self.assertTrue('; SameSite=None; Secure' in cookies_string[2])
