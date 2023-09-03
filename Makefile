.PHONY: clean-pyc clean-build docs help
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
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc clean-output

clean-output:
	rm -f output/*

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint: ## check style with flake8
	flake8 django_test_tools tests

test: clean-output ## run tests quickly with the default Python
	python manage.py test --settings tests.settings

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source django_test_tools runtests.py tests
	coverage report -m
	coverage html
	open htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/django-test-tools.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ django_test_tools
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

sdist: clean # test
	python setup.py sdist
	python setup.py sdist bdist_wheel
	ls -l dist

patch: clean ## package and upload a release
	python ./scripts/bump.py --action=patch

minor: clean ## package and upload a release
	python ./scripts/bump.py --action=minor

upload: sdist
	git push origin master
	git push origin develop
	git push --tags
	twine upload ./dist/*

travis-push: clean
	python setup.py sdist
	python setup.py sdist bdist_wheel
	ls -l dist
	git push --tags
	git push origin master
	git push origin develop

