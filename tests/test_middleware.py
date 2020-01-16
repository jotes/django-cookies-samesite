import unittest

from mock import patch

from django.http import HttpResponse

from django.test import TestCase


class CookiesSamesiteTests(TestCase):
    def test_cookie_samesite_strict(self):
        with self.settings(SESSION_COOKIE_SAMESITE='strict'):
            response = self.client.get('/cookies-test/')

            self.assertEqual(response.cookies['sessionid']['samesite'], 'strict')
            self.assertEqual(response.cookies['csrftoken']['samesite'], 'strict')

            csrf_token = response.cookies['csrftoken']
            session_id = response.cookies['sessionid']

            cookies_string = sorted(response.cookies.output().split('\r\n'))
            self.assertTrue('csrftoken=', cookies_string[0])
            self.assertTrue('; SameSite=strict', cookies_string[0])
            self.assertTrue('sessionid=', cookies_string[2])
            self.assertTrue('; SameSite=strict', cookies_string[2])

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

    @unittest.skip('@TODO')
    def test_cookie_samesite_django21(self):
        # Raise DeprecationWarning for newer versions of Django

        with patch('django.__version__', return_value='2.1.0'):
            with self.assertRaises(DeprecationWarning) as exc:
                self.client.get('/cookies-test/')

            self.assertEqual(exc.exception.args[0], (
                'Your version of Django supports SameSite flag in cookies. '
                'You should remove django-cookies-samesite from your project.'
            ))

        with patch('django_cookies_samesite.middleware.django.__version__', return_value='2.3.0'):
            with self.assertRaises(DeprecationWarning) as exc:
                self.client.get('/cookies-test/')

            self.assertEqual(exc.exception.args[0], (
                'Your version of Django supports SameSite flag in cookies. '
                'You should remove django-cookies-samesite from your project.'
            ))

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

    def test_cookie_samesite_invalid(self):
        with self.settings(SESSION_COOKIE_SAMESITE='invalid'):
            with self.assertRaises(ValueError) as exc:
                self.client.get('/cookies-test/')

            self.assertEqual(exc.exception.args[0], 'samesite must be "lax", "none", or "strict".')

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
