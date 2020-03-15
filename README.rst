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

Supports Python 3.6, 3.7 with Django 1.11.29, 2.2.11 and 3.0.4


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


in the settings.py file add an ouput folder (make sure it exists):

.. code-block:: python

    TEST_OUTPUT_PATH = ROOT_DIR.path('output').root


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

File utilities
+++++++++++++++

This method decorator creates a filename with date using the provided extension and delete the file after the method has been executed.

The settings.TEST_OUTPUT_PATH must be configured in your settings file.

    .. code-block:: python

        @temporary_file('json')
        def test_temporary_file_decorator(self):
            filename = self.test_temporary_file_decorator.filename
            ... write to the file ...


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Builds
------
1. Setup environment

.. code-block:: bash
    source ~/python_envs/django_test_tools_env/bin/activate


2. Updated version. Instead of patch you could also use **major** o **minor** depending on the level of the release.

.. code-block:: bash

    $ make patch


3. Check the .travis.yml to make sure the versions of Djago are the latests. Check in https://www.djangoproject.com/download/
for the latest versions.

4. Check setup.py for Django and Python versions.

5. Close the git-flow release manually.

6. Upload the new version to pypi

.. code-block:: bash

    make upload


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
