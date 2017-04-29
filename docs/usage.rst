=====
Usage
=====

To use Django Test Tools in a project, add it to your `INSTALLED_APPS`:

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
