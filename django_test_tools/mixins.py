import csv
import json
import os
from io import StringIO

from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient

from .excel import ExcelAdapter
from .exceptions import DjangoTestToolsException


class TestCommandMixin(object):
    """
    This mixin helps capture the output of a command written with the stdout.write() method and
     the stderr.write

    .. code-block:: python

        class TestYourCommand(TestCommandMixin, TestCase):

            def test_your_command_action(self):
                call_command('your_command', 'your_argument', stdout=self.content, stderr=self.error_content)
                results = self.get_results()
                self.assertEqual(23, len(results))
    """

    # noinspection PyPep8Naming
    def setUp(self):
        self.content = StringIO()
        self.error_content = StringIO()

    def get_results(self, content=None):
        if content is None:
            content = self.content
        content.seek(0)
        lines = content.readlines()
        results = list()
        for line in lines:
            results.append(line.strip('\n'))
        return results

    def get_errors(self):
        return self.get_results(self.error_content)


class TestOutputMixin(object):
    clean_output = True

    def clean_output_folder(self, dated_filename):
        if self.clean_output:
            os.remove(dated_filename)
            # noinspection PyUnresolvedReferences
            self.assertFalse(os.path.exists(dated_filename))

    def get_excel_content(self, filename, sheet_name=None):
        """
        Reads the content of an excel file and returns the content a as list of row lists.
        :param filename: string full path to the filename
        :param sheet_name: string. Name of the sheet to read if None will read the active sheet
        :return: a list containing a list of values for every row.
        """
        adapter = ExcelAdapter()
        return adapter.convert_to_list(filename, sheet_name)

    def get_csv_content(self, filename, delimiter=',', encoding='utf-8'):
        content = list()
        with open(filename, 'r', encoding=encoding) as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            for row in reader:
                content.append(row)
        return content

    def get_txt_content(self, filename, encoding='utf-8'):
        content = list()
        with open(filename, 'r', encoding=encoding) as file:
            lines = file.readlines()
        for line in lines:
            content.append(line.strip('\n'))
        return content


class JWTTestMixin(object):

    def get_access_token(self, user):
        token_url = reverse('token_obtain_pair')
        pay_load = {'username': user.username, 'password': 'password'}
        token_response = self.post(token_url, data=pay_load)
        access_token = token_response.data['access']
        return access_token

    def get_with_token(self, url, access_token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
        response = client.get(url, data={'format': 'json'})
        return response

    def delete_with_token(self, url, access_token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
        response = client.delete(url, data={'format': 'json'})
        return response

    def put_with_token(self, url, access_token, data):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
        response = client.put(url, data=data)
        return response


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
