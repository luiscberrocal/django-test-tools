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

.. image:: https://readthedocs.org/projects/django-test-tools/badge/?version=latest
    :target: https://django-test-tools.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Simple tests tools to make testing faster and easier. Most of the tools are to do a quick scaffolding for tests.

The tools presume a naming convention:

- **Tests:** Are named with the convention **TestCaseModelName**. For a model named *Poll* the test would be generated
  as the testing class would be *TestCasePoll*
- **Factories:** Are named with the convention **ModelName**. For a model named *Poll* the test would be generated
  as the testing class would be *PollFactory*
- **Serializers:** Are named with the convention **TestCaseSerializer**. For a model named *Poll* the test would be generated
  as the testing class would be *PollSerializer*


Compatibility matrix:

+----------------+---------------+--------------+--------------+
| Python version | Django 1.11.x | Django 2.2.x | Django 3.0.x |
+----------------+---------------+--------------+--------------+
|       3.7      |       x       |       x      |       x      |
+----------------+---------------+--------------+--------------+
|       3.6      |       x       |       x      |       x      |
+----------------+---------------+--------------+--------------+

Documentation
-------------

The full documentation is at https://django-test-tools.readthedocs.io.

Quickstart
----------

Install Django Test Tools:

.. code-block:: bash

    pip install django-test-tools


In your settings.py file add it to your `INSTALLED_APPS`

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_test_tools',
        ...
    )


Add the settings variable **TEST_OUTPUT_PATH**

.. code-block:: python

    import environ

    ROOT_DIR = (
        environ.Path(__file__) - 3
    )  # (alpha_clinic/config/settings/base.py - 3 = alpha_clinic/)
    APPS_DIR = ROOT_DIR.path("myapp")
    TEST_OUTPUT_PATH = ROOT_DIR.path("output").root

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


Pushing code to Pypi
--------------------
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
