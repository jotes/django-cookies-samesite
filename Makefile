.PHONY: clean-pyc clean-build docs help black black-check
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
USER_NAME := $(shell id -u -n)
BROWSER := python -c "$$BROWSER_PYSCRIPT"
BUMPVERSION := docker run \
   --env USER  --env USER_ID=`id -u` \
   --env GROUP --env GROUP_ID=`id -g` \
   --interactive --tty --rm \
   --volume $(shell pwd):/home/$(USER_NAME)/host  \
   -v ~/.gitconfig:/etc/gitconfig \
   -w /home/$(USER_NAME)/host \
   jesuspv/bumpversion --config-file setup.cfg


help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +


black: ## format all files with Black
	black django_cookies_samesite

black-check: ## check if python files are correctly formatted
	black --check django_cookies_samesite

flake8: ## check style with flake8
	flake8 django_cookies_samesite tests

test: ## run tests quickly with the default Python
	python runtests.py tests

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source django_cookies_samesite runtests.py tests
	coverage report -m
	coverage html
	open htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/django-cookies-samesite.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ django_cookies_samesite
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

sdist: clean ## package
	python setup.py sdist
	ls -l dist

bump: part?=minor
bump: ## Relese a new version
	$(BUMPVERSION) $(part)
