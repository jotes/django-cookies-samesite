=====
Usage
=====

To use django-cookies-samesite in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_cookies_samesite.apps.DjangoCookiesSamesiteConfig',
        ...
    )

Add django-cookies-samesite's URL patterns:

.. code-block:: python

    from django_cookies_samesite import urls as django_cookies_samesite_urls


    urlpatterns = [
        ...
        url(r'^', include(django_cookies_samesite_urls)),
        ...
    ]
