=============================
django-cookies-samesite
=============================

.. image:: https://badge.fury.io/py/django-cookies-samesite.svg
    :target: https://badge.fury.io/py/django-cookies-samesite

.. image:: https://travis-ci.org/jotes/django-cookies-samesite.svg?branch=master
    :target: https://travis-ci.org/jotes/django-cookies-samesite

.. image:: https://codecov.io/gh/jotes/django-cookies-samesite/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jotes/django-cookies-samesite

Repository status
-----------------
The project isn't actively maintained anymore. If you want to help and add a link to your fork, add it there: https://github.com/jotes/django-cookies-samesite/issues/50 .

Description
-----------


This repository contains a middleware which automatically sets SameSite attribute for session and csrf cookies in legacy versions of Django e.g. 1.11.x, 2.2.x or 3.0.x.

This module is not needed for Django 3.1.x which introduces full support of SameSite flag for session and csrf cookie. 


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

.. important::
    If you're planning to use this middleware together with the newer version of Django (>3.0.x), and you want to e.g.
    set the SameSite attribute to `none`, then you have to add `DCS_` prefix to all `django-cookies-samesite` settings (see examples below).

    It will help you to avoid bugs caused by the conflicting settings names.

    Related bug:
    https://github.com/jotes/django-cookies-samesite/issues/19



Set your preferred SameSite policy in `settings.py`:

.. code-block:: python

   SESSION_COOKIE_SAMESITE = 'lax'
   # or
   DCS_SESSION_COOKIE_SAMESITE = 'Lax'

This can be 'Lax', 'None', 'Strict', or None to disable the flag.
Also, you can set this flag in your custom cookies:

.. code-block:: python

   SESSION_COOKIE_SAMESITE_KEYS = {'my-custom-cookies'}
   # or
   DCS_SESSION_COOKIE_SAMESITE_KEYS = {'my-custom-cookies'}

After that you should be able to see the SameSite flag set for session and csrf cookies.

You can set the SameSite flag on all cookies (even on those coming from third-party Django apps):

.. code-block:: python

    SESSION_COOKIE_SAMESITE_FORCE_ALL = True
    # or
    DCS_SESSION_COOKIE_SAMESITE_FORCE_ALL = True

The `sessionid` and `csrftoken` cookies are automatically handled by the middleware. This behavior can be disabled with:

.. code-block:: python

   SESSION_COOKIE_SAMESITE_FORCE_CORE = False
   # or
   DCS_SESSION_COOKIE_SAMESITE_FORCE_CORE = False

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

Contributors
------------
* Abdul Rafiu <rafiu.rahim@gmail.com>
* Code Hugger (Matthew Jones) <jonespm@umich.edu>
* Jarosław Śmiejczak <poke@jotes.work>
* Jørn Lomax <northlomax@gmail.com>
* Liuyang Wan <noreply@github.com>
* Mykolas Kvieska <noreply@github.com>
* Tim McCormack <tmccormack@edx.org>
