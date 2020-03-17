import unittest

from mock import patch

import django

from ddt import ddt, data
from django.test import TestCase

from django_cookies_samesite.middleware import DJANGO_SUPPORTED_VERSION


@ddt
class CookiesSamesiteTests(TestCase):
    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_samesite_strict(self):
        with self.settings(SESSION_COOKIE_SAMESITE='strict'):
            response = self.client.get('/cookies-test/')

            self.assertEqual(response.cookies['sessionid']['samesite'], 'strict')
            self.assertEqual(response.cookies['csrftoken']['samesite'], 'strict')

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('csrftoken=', cookies_string[0])
            self.assertTrue('; SameSite=strict', cookies_string[0])
            self.assertTrue('sessionid=', cookies_string[2])
            self.assertTrue('; SameSite=strict', cookies_string[2])

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_samesite_lax(self):
        with self.settings(SESSION_COOKIE_SAMESITE='lax'):
            response = self.client.get('/cookies-test/')

            self.assertEqual(response.cookies['sessionid']['samesite'], 'lax')
            self.assertEqual(response.cookies['csrftoken']['samesite'], 'lax')
            cookies_string = sorted(response.cookies.output().split('\r\n'))

            self.assertTrue('csrftoken=' in cookies_string[0])
            self.assertTrue('; SameSite=lax' in cookies_string[0])
            self.assertTrue('sessionid=' in cookies_string[2])
            self.assertTrue('; SameSite=lax' in cookies_string[2])

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_samesite_none(self):
        with self.settings(SESSION_COOKIE_SAMESITE='none'):
            response = self.client.get('/cookies-test/')

            self.assertEqual(response.cookies['sessionid']['samesite'], 'none')
            self.assertEqual(response.cookies['csrftoken']['samesite'], 'none')
            cookies_string = sorted(response.cookies.output().split('\r\n'))

            self.assertTrue('csrftoken=' in cookies_string[0])
            self.assertTrue('; SameSite=none' in cookies_string[0])
            self.assertTrue('sessionid=' in cookies_string[2])
            self.assertTrue('; SameSite=none' in cookies_string[2])

        with self.settings(SESSION_COOKIE_SAMESITE='none', SESSION_COOKIE_SAMESITE_FORCE_ALL=True):
            response = self.client.get('/cookies-test/')

            self.assertEqual(response.cookies['sessionid']['samesite'], 'none')
            self.assertEqual(response.cookies['csrftoken']['samesite'], 'none')
            self.assertEqual(response.cookies['custom_cookie']['samesite'], 'none')
            self.assertEqual(response.cookies['zcustom_cookie']['samesite'], 'none')

            cookies_string = sorted(response.cookies.output().split('\r\n'))

            self.assertTrue('custom_cookie=' in cookies_string[1])
            self.assertTrue('; SameSite=none' in cookies_string[1])
            self.assertTrue('csrftoken=' in cookies_string[0])
            self.assertTrue('; SameSite=none' in cookies_string[0])
            self.assertTrue('sessionid=' in cookies_string[2])
            self.assertTrue('; SameSite=none' in cookies_string[2])
            self.assertTrue('zcustom_cookie=' in cookies_string[3])
            self.assertTrue('; SameSite=none' in cookies_string[3])

    @unittest.skipIf(django.get_version() < DJANGO_SUPPORTED_VERSION, 'should skip if Django does not support')
    def test_cookie_samesite_django30(self):
        # Raise DeprecationWarning for newer versions of Django

        with patch('django.get_version', return_value=DJANGO_SUPPORTED_VERSION):
            with self.assertRaises(DeprecationWarning) as exc:
                self.client.get('/cookies-test/')

            # print(exc.exception.args)
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
            SESSION_COOKIE_SAMESITE='lax',
            SESSION_COOKIE_SAMESITE_KEYS='something'
        ):
            with self.assertRaises(ValueError) as exc:
                self.client.get('/cookies-test/')

            self.assertEqual(exc.exception.args[0], 'SESSION_COOKIE_SAMESITE_KEYS should be a list, set or tuple.')

        # Test if SameSite flags is set to custom cookies
        with self.settings(
            SESSION_COOKIE_SAMESITE='lax',
            SESSION_COOKIE_SAMESITE_KEYS=('custom_cookie',)
        ):
            response = self.client.get('/cookies-test/')

            self.assertEqual(response.cookies['sessionid']['samesite'], 'lax')
            self.assertEqual(response.cookies['csrftoken']['samesite'], 'lax')
            self.assertEqual(response.cookies['custom_cookie']['samesite'], 'lax')
            self.assertEqual(response.cookies['zcustom_cookie']['samesite'], '')

            cookies_string = sorted(response.cookies.output().split('\r\n'))

            self.assertTrue('custom_cookie=' in cookies_string[1])
            self.assertTrue('; SameSite=lax' in cookies_string[1])
            self.assertTrue('csrftoken=' in cookies_string[0])
            self.assertTrue('; SameSite=lax' in cookies_string[0])
            self.assertTrue('sessionid=' in cookies_string[2])
            self.assertTrue('; SameSite=lax' in cookies_string[2])
            self.assertTrue('zcustom_cookie=' in cookies_string[3])
            self.assertTrue('; SameSite=lax' not in cookies_string[3])

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_samesite_invalid(self):
        with self.settings(SESSION_COOKIE_SAMESITE='invalid'):
            with self.assertRaises(ValueError) as exc:
                self.client.get('/cookies-test/')

            self.assertEqual(exc.exception.args[0], 'samesite must be "lax", "none", or "strict".')

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_samesite_unset(self):
        with self.settings(SESSION_COOKIE_SAMESITE=None):
            response = self.client.get('/cookies-test/')
            print(response.cookies)
            self.assertEqual(response.cookies['sessionid'].get('samesite'), '')
            self.assertEqual(response.cookies['csrftoken'].get('samesite'), '')

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('csrftoken=' in cookies_string[0])
            self.assertTrue('; SameSite=lax' not in cookies_string[0])
            self.assertTrue('; SameSite=strict' not in cookies_string[0])
            self.assertTrue('sessionid=' in cookies_string[2])
            self.assertTrue('; SameSite=lax' not in cookies_string[2])
            self.assertTrue('; SameSite=strict' not in cookies_string[2])

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_cookie_names_changed(self):
        session_name = 'sessionid-test'
        csrf_name = 'csrftoken-test'
        with self.settings(
            SESSION_COOKIE_NAME=session_name,
            CSRF_COOKIE_NAME=csrf_name,
            SESSION_COOKIE_SAMESITE='lax'
        ):
            response = self.client.get('/cookies-test/')

            self.assertEqual(response.cookies[session_name]['samesite'], 'lax')
            self.assertEqual(response.cookies[csrf_name]['samesite'], 'lax')
            cookies_string = sorted(response.cookies.output().split('\r\n'))

            self.assertTrue(csrf_name + '=' in cookies_string[0])
            self.assertTrue('; SameSite=lax' in cookies_string[0])
            self.assertTrue(session_name + '=' in cookies_string[2])
            self.assertTrue('; SameSite=lax' in cookies_string[2])

    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
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
            SESSION_COOKIE_SAMESITE='lax'
        ):
            response = self.client.get(
                '/cookies-test/',
                HTTP_USER_AGENT=ua_string,
            )
            self.assertEqual(response.cookies[session_name]['samesite'], '')
            self.assertEqual(response.cookies[csrf_name]['samesite'], '')

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('; SameSite=lax' not in cookies_string[0])
            self.assertTrue('; SameSite=lax' not in cookies_string[1])

    @data(
        # Chrome
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2704.103 Safari/537.36",
        # Firefox
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
        # Internet Explorer
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)",
        # Safari
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"  # noqa
    )
    @unittest.skipIf(django.get_version() >= DJANGO_SUPPORTED_VERSION, 'should skip if Django already supports')
    def test_supported_browsers(self, ua_string):
        session_name = 'sessionid-test'
        csrf_name = 'csrftoken-test'

        with self.settings(
            SESSION_COOKIE_NAME=session_name,
            CSRF_COOKIE_NAME=csrf_name,
            SESSION_COOKIE_SAMESITE='lax'
        ):
            response = self.client.get(
                '/cookies-test/',
                HTTP_USER_AGENT=ua_string,
            )
            self.assertEqual(response.cookies[session_name]['samesite'], 'lax')
            self.assertEqual(response.cookies[csrf_name]['samesite'], 'lax')

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('; SameSite=lax' in cookies_string[0])
            self.assertTrue('; SameSite=lax' in cookies_string[2])
