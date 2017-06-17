=============================
Django Test Tools
=============================

.. image:: https://badge.fury.io/py/django-test-tools.svg
    :target: https://badge.fury.io/py/django-test-tools

.. image:: https://travis-ci.org/luiscberrocal/django-test-tools.svg?branch=master
    :target: https://travis-ci.org/luiscberrocal/django-test-tools

.. image:: https://codecov.io/gh/luiscberrocal/django-test-tools/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/luiscberrocal/django-test-tools

Simple tests tools to make testing faster and easier.

Supports Python 3.4, 3.5, 3.5 with Django 1.10.7 and 1.11.2.


Documentation
-------------

The full documentation is at https://django-test-tools.readthedocs.io.

Quickstart
----------

Install Django Test Tools::

    pip install django-test-tools

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_test_tools.apps.DjangoTestToolsConfig',
        ...
    )

Add Django Test Tools's URL patterns:

.. code-block:: python

    from django_test_tools import urls as django_test_tools_urls


    urlpatterns = [
        ...
        url(r'^', include(django_test_tools_urls)),
        ...
    ]

Features
--------

Factory Generator
++++++++++++++++++

.. code-block:: bash

    $  $ python manage.py generate_factories project.app

Model Test Case Generator
+++++++++++++++++++++++++

.. code-block:: bash

    $  $ python manage.py generate_model_test_cases project.app

Serializer Generator
++++++++++++++++++++

.. code-block:: bash

    $ python manage.py generate_serializers project.app -s ModelSerializer

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Builds
------


Run bumpversion

.. code-block:: bash

    $ bumpversion minor


Instead of minor you could also use **major** o **patch** depending on the level of the release.

.. code-block:: bash

    python setup.py sdist bdist_wheel

    python setup.py register -r pypitest

    python setup.py sdist upload -r pypitest


.. code-block:: bash

    python setup.py register -r pypi

    python setup.py sdist upload -r pypi

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
