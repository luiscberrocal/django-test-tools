#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from django_test_tools/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)

    with open(filename) as fn:
        version_file = fn.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("django_test_tools", "__init__.py")

if sys.argv[-1] == 'publish':
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

with open('README.rst') as rf:
    readme = rf.read()

with open('HISTORY.rst') as hf:
    history = hf.read().replace('.. :changelog:', '')

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='django-test-tools',
    version=version,
    description="""Simple tests tools to make testing faster and easier.""",
    long_description=readme + '\n\n' + history,
    author='Luis Carlos Berrocal',
    author_email='luis.berrocal.1942@gmail.com',
    url='https://github.com/luiscberrocal/django-test-tools',
    packages=[
        'django_test_tools',
    ],
    include_package_data=True,
    install_requires=required,
    license="MIT",
    zip_safe=False,
    keywords='django-test-tools',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
