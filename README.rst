=============================
django-cookies-samesite
=============================

.. image:: https://badge.fury.io/py/django-cookies-samesite.svg
    :target: https://badge.fury.io/py/django-cookies-samesite

.. image:: https://travis-ci.org/jotes/django-cookies-samesite.svg?branch=master
    :target: https://travis-ci.org/jotes/django-cookies-samesite

.. image:: https://codecov.io/gh/jotes/django-cookies-samesite/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jotes/django-cookies-samesite

Django 2.1.x introduces support of SameSite flag for session and csrf cookie.

Unfortunately, this functionality will not be ported to older versions of Django e.g. 1.11.x.

This repository contains a middleware which automatically sets SameSite attribute for session and csrf cookies in legacy versions of Django.

Quickstart
----------

Install django-cookies-samesite::

    pip install django-cookies-samesite

Add the middleware to the top of `MIDDLEWARE_CLASSES`:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        'django_cookies_samesite.middleware.CookiesSameSite',
        ...
    )

Set your preferred SameSite policy in `settings.py`:

.. code-block:: python

   SESSION_COOKIE_SAMESITE = 'Lax'

This can be 'Lax', 'None', 'Strict', or None to disable the flag.

Also, you can set this flag in your custom cookies:

.. code-block:: python

   SESSION_COOKIE_SAMESITE_KEYS = {'my-custom-cookies'}


After that you should be able to see SameSite flag set for session and csrf cookies:
![screenshot]()

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
