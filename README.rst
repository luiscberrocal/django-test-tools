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

Supports Python 3.4, 3.5, 3.6 with Django 1.10.7, 1.11.x and 2.1.x


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

Create a release using git-flow

Update setup.py. Make sure the versions in **install_requies** matches the content of the requirements.txt file.

Run bumpversion

.. code-block:: bash

    $ bumpversion minor

Check the .travis.yml to make sure the versions of Djago are the latests. Check in https://www.djangoproject.com/download/
for the latest versions.

Close the git-flow release.

Push develop and master to the repository.

Push the tags

.. code-block:: bash

    $ git push --tags


Instead of minor you could also use **major** o **patch** depending on the level of the release.

.. code-block:: bash

    make sdist


To publish to pypi run:


.. code-block:: bash

    twine upload ./dist/*

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
