=====
Usage
=====

To use Django Test Tools in a project, add it to your `INSTALLED_APPS`:

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
variable **TEST_OUTPUT_PATH** point to it.

.. code-block:: python

    import environ

    ROOT_DIR = (
        environ.Path(__file__) - 3
    )  #
    APPS_DIR = ROOT_DIR.path("my_project")
    TEST_OUTPUT_PATH = ROOT_DIR.path("output").root
