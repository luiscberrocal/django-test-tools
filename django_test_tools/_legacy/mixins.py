import json

from django.conf import settings

from django_test_tools.exceptions import DjangoTestToolsException


class TestFixtureMixin(object):
    """
    This a mixin to add to test cases to easily access fixtures. It assumes the the you have a package for your tests
    named **tests** and your **fixtures** are in a folder named fixtures within your tests package and that you have
    settings variable named APPS_DIR pointing tou your applications folder (this is created by Cookiecutter by default).
    Your tests package should look like this.

    |   ├── clinics
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── exceptions.py
    │   ├── forms.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── factories.py
    │   │   ├── fixtures
    │   │   │   ├── data.json
    │   │   │   ├── model_data.txt
    │   │   ├── test_forms.py
    │   │   ├── test_models.py
    │   ├── urls.py
    │   └── views.py

    For the above exmple

    .. code-block:: python

        class TestClinicAdapter(TestFixtureMixin, TestCase):

            def setUp(self) -> None:
                self.app_name = 'clinics'

            def test_parse(self):
                clinics_dictionary = self.get_fixture_json('data.json')
                ...

            def test_read(self):
                filename = self.get_fixture_fullpath('model.txt')
                ...

    """
    app_name = None

    def __init__(self, app_name=None, **kwargs):
        self.app_name = app_name
        ## this is to test and allow app_name to be None.
        self.strict = kwargs.get('strict', True)

    def get_fixture_fullpath(self, fixture_filename):
        """
        Get full patch for the fixture file

        :param fixture_filename: <str> name of the fixture file
        :return: <str> full path to fixture file
        """
        self._sanity_check()
        if self.app_name is None:
            fixture_file = settings.APPS_DIR.path('tests', 'fixtures', fixture_filename).root
        else:
            fixture_file = settings.APPS_DIR.path(self.app_name, 'tests', 'fixtures', fixture_filename).root
        return fixture_file

    def get_fixture_json(self, fixture_filename):
        """
        Reads a file and returns the json content.

        :param fixture_filename: <str> filename
        :return: <dict> With the file content
        """
        fixture_file = self.get_fixture_fullpath(fixture_filename)

        with open(fixture_file, 'r') as f:
            json_data = json.load(f)
        return json_data

    def _sanity_check(self):
        if self.app_name is None and self.strict:
            raise DjangoTestToolsException('app_name not defined')
        if not hasattr(settings, 'APPS_DIR'):
            raise DjangoTestToolsException('APPS_DIR not defined')
