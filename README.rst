=============================
Django Test Tools
=============================

.. image:: https://badge.fury.io/py/django-test-tools.svg
    :target: https://badge.fury.io/py/django-test-tools

.. image:: https://travis-ci.org/luiscberrocal/django-test-tools.svg?branch=master
    :target: https://travis-ci.org/luiscberrocal/django-test-tools

.. image:: https://codecov.io/gh/luiscberrocal/django-test-tools/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/luiscberrocal/django-test-tools

.. image:: https://landscape.io/github/luiscberrocal/django-test-tools/master/landscape.svg?style=flat
   :target: https://landscape.io/github/luiscberrocal/django-test-tools/master
   :alt: Code Health

.. image:: https://pyup.io/repos/github/luiscberrocal/django-test-tools/shield.svg
     :target: https://pyup.io/repos/github/luiscberrocal/django-test-tools/
     :alt: Updates


Simple tests tools to make testing faster and easier.

Supports Python 3.5, 3.6, 3.7 with Django 1.10.8, 1.11.x, 2.0,x, 2.1.x adn 2.2.x


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
        'django_test_tools',
        ...
    )





Features
--------

Factory Generator
++++++++++++++++++

.. code-block:: bash

    $  python manage.py generate_factories project.app

Model Test Case Generator
+++++++++++++++++++++++++

.. code-block:: bash

    $  python manage.py generate_model_test_cases project.app

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

.. code-block:: bash

    $ make patch

Check the .travis.yml to make sure the versions of Djago are the latests. Check in https://www.djangoproject.com/download/
for the latest versions.

Close the git-flow release.

Instead of patch you could also use **major** o **minor** depending on the level of the release.

.. code-block:: bash

    make upload


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
