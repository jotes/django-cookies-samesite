#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from django_cookies_samesite/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("django_cookies_samesite", "__init__.py")


if sys.argv[-1] == "publish":
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == "tag":
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")

setup(
    name="django-cookies-samesite-fork",
    version=version,
    description="Middleware which sets SameSite flag for session and csrf "
    "cookies in legacy versions of Django. Forked from "
    "https://pypi.org/project/django-cookies-samesite/",
    long_description=readme + "\n\n" + history,
    author="Antoine Lefebvre-Brossard",
    author_email="antoine@protonmail.com",
    url="https://github.com/SALTISES4/django-cookies-samesite",
    packages=["django_cookies_samesite"],
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
    keywords="django-cookies-samesite",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 1.11",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
