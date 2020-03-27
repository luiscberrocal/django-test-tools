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
        'django_test_tools.apps.DjangoTestToolsConfig',
        ...
    )


Create an output folder in the root folder of you project, name it what ever you want, and add the settings
variable **TEST_OUTPUT_PATH** pointing to it.

.. code-block:: python

    import environ

    ROOT_DIR = (
        environ.Path(__file__) - 3
    )  # (my_project/config/settings/base.py - 3 = alpha_clinic/)
    APPS_DIR = ROOT_DIR.path("my_project")
    TEST_OUTPUT_PATH = ROOT_DIR.path("output").root

Features
--------

Factory Generator
++++++++++++++++++

To create `Factory Boy`_ style factories.

For a django project named polling_app with an app name poll the following command will generate the scaffolding for
the tests for all the models in th app polls.

.. code-block:: bash

    $  python manage.py generate_factories polling_app.polls


For the following models


.. code-block:: python

    class OperatingSystem(models.Model):
        name = models.CharField(max_length=20)
        version = models.CharField(max_length=5)
        licenses_available = models.IntegerField()
        cost = models.DecimalField(decimal_places=2, max_digits=7)

        class Meta:
            unique_together = ('name', 'version')


    class Server(models.Model):
        PRODUCTION = 'PROD'
        DEVELOPMENT = 'DEV'
        USE_CHOICES = ((PRODUCTION, 'Prod'),
                       (DEVELOPMENT, 'Dev'))
        name = models.CharField(max_length=20, unique=True)
        notes = models.TextField()
        virtual = models.BooleanField()
        ip_address = models.GenericIPAddressField()
        created = models.DateTimeField()
        online_date = models.DateField()
        operating_system = models.ForeignKey(OperatingSystem, related_name='servers', on_delete=models.CASCADE)
        server_id = models.CharField(max_length=6)
        use = models.CharField(max_length=4, choices=USE_CHOICES, default=DEVELOPMENT)
        comments = models.TextField(null=True, blank=True)


running `python manage.py generate_factories example.servers > ./output/factories.py` will create the following factories

.. code-block:: python

    import string

    from random import randint
    from pytz import timezone

    from django.conf import settings

    from factory import Iterator
    from factory import LazyAttribute
    from factory import SubFactory
    from factory import lazy_attribute
    from factory.django import DjangoModelFactory, FileField
    from factory.fuzzy import FuzzyText, FuzzyInteger
    from faker import Factory as FakerFactory

    from example.servers.models import OperatingSystem, Server

    faker = FakerFactory.create()


    class OperatingSystemFactory(DjangoModelFactory):
        class Meta:
            model = OperatingSystem

        name = LazyAttribute(lambda x: faker.text(max_nb_chars=20))
        version = LazyAttribute(lambda x: faker.text(max_nb_chars=5))
        licenses_available = LazyAttribute(lambda o: randint(1, 100))
        cost = LazyAttribute(lambda x: faker.pydecimal(left_digits=5, right_digits=2, positive=True))

    class ServerFactory(DjangoModelFactory):
        class Meta:
            model = Server

        name = LazyAttribute(lambda x: faker.text(max_nb_chars=20))
        notes = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
        virtual = Iterator([True, False])
        ip_address = LazyAttribute(lambda o: faker.ipv4(network=False))
        created = LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", end_date="now",
                                                               tzinfo=timezone(settings.TIME_ZONE)))
        online_date = LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", end_date="now",
                                                               tzinfo=timezone(settings.TIME_ZONE)))
        operating_system = SubFactory(OperatingSystemFactory)
        server_id = LazyAttribute(lambda x: FuzzyText(length=6, chars=string.digits).fuzz())
        use = Iterator(Server.CHOICES, getter=lambda x: x[0])
        comments = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))

Important the use attribute is created incorrectly. **When you use choices you need to manually change it** to USE_CHOICES.

.. code-block:: python

        use = Iterator(Server.USE_CHOICES, getter=lambda x: x[0])


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
.. _`Factory Boy`: https://factoryboy.readthedocs.io/en/latest/
