from unittest import mock

from django.test import SimpleTestCase

from django_test_tools.assert_utils import write_assertions
from django_test_tools.file_utils import temporary_file
from django_test_tools.pip.utils import parse_specifier, read_requirement_file, list_outdated_libraries, \
    update_outdated_libraries, get_latest_version, list_libraries
from tests.mixins import TestFixtureMixin


class TestParseSpecifier(SimpleTestCase):
    def test_parse_specifier(self):
        result = parse_specifier('==2.1.1')
        self.assertEqual(result[0], '==')
        self.assertEqual(result[1], '2.1.1')

    def test_parse_specifier(self):
        with self.assertRaises(ValueError) as context:
            parse_specifier('2.1.1')

        self.assertEqual(str(context.exception), 'Invalid speficier "2.1.1"')

    @mock.patch('django_test_tools.pip.utils.subprocess.check_output')
    def test_list_outdated_libraries(self, mock_pip_main):
        main_result = b'binaryornot (0.4.3) - Latest: 1.4.4 [wheel]\nchardet (3.0.2) - Latest: 3.0.4 [wheel]\n' \
                       b'cookiecutter (1.5.1) - Latest: 1.6.0 [wheel]\ncoverage (4.4.1) - Latest: 4.4.2 [wheel]\n' \
                       b'Faker (0.7.17) - Latest: 0.8.7 [wheel]\nflake8 (3.3.0) - Latest: 3.5.0 [wheel]\n' \
                       b'Jinja2 (2.9.6) - Latest: 2.10 [wheel]\nopenpyxl (2.4.8) - Latest: 2.4.9 [sdist]\n' \
                       b'pbr (3.0.1) - Latest: 3.1.1 [wheel]\npluggy (0.4.0) - Latest: 0.5.2 [sdist]\n' \
                       b'py (1.4.33) - Latest: 1.5.2 [wheel]\npyflakes (1.5.0) - Latest: 1.6.0 [wheel]\n' \
                       b'pylint (1.7.2) - Latest: 1.7.4 [wheel]\npython-dateutil (2.6.0) - Latest: 2.6.1 [wheel]\n' \
                       b'pytz (2017.2) - Latest: 2017.3 [wheel]\nradon (2.0.2) - Latest: 2.1.1 [wheel]\n' \
                       b'requests (2.14.2) - Latest: 2.18.4 [wheel]\nsetuptools (36.0.1) - Latest: 37.0.0 [wheel]\n' \
                       b'six (1.10.0) - Latest: 1.11.0 [wheel]\ntox (2.7.0) - Latest: 2.9.1 [wheel]\n' \
                       b'wrapt (1.10.10) - Latest: 1.10.11 [sdist]\n' \
                       b'DEPRECATION: The default format will switch to columns in the future. '  \
                       b'You can use --format=(legacy|columns) (or define a format=(legacy|columns) in your pip.conf '  \
                       b'under the [list] section) to disable this warning.\n'

        mock_capture = mock.Mock()
        mock_capture.return_value = main_result


        with mock.patch('django_test_tools.pip.utils.subprocess.check_output', mock_capture):
            outdated = list_outdated_libraries()
        #mock_pip_main.assert_called_with(['list', b'--outdated'])

        self.assertEqual(len(outdated), 21)
        self.assertEqual(outdated[0]['current_version'], '0.4.3')
        self.assertEqual(outdated[0]['name'], 'binaryornot')
        self.assertEqual(outdated[0]['new_version'], '1.4.4')
        self.assertEqual(outdated[1]['current_version'], '3.0.2')
        self.assertEqual(outdated[1]['name'], 'chardet')
        self.assertEqual(outdated[1]['new_version'], '3.0.4')
        self.assertEqual(outdated[2]['current_version'], '1.5.1')
        self.assertEqual(outdated[2]['name'], 'cookiecutter')
        self.assertEqual(outdated[2]['new_version'], '1.6.0')
        self.assertEqual(outdated[3]['current_version'], '4.4.1')
        self.assertEqual(outdated[3]['name'], 'coverage')
        self.assertEqual(outdated[3]['new_version'], '4.4.2')
        self.assertEqual(outdated[4]['current_version'], '0.7.17')
        self.assertEqual(outdated[4]['name'], 'faker')
        self.assertEqual(outdated[4]['new_version'], '0.8.7')
        self.assertEqual(outdated[5]['current_version'], '3.3.0')
        self.assertEqual(outdated[5]['name'], 'flake8')
        self.assertEqual(outdated[5]['new_version'], '3.5.0')
        self.assertEqual(outdated[6]['current_version'], '2.9.6')
        self.assertEqual(outdated[6]['name'], 'jinja2')
        self.assertEqual(outdated[6]['new_version'], '2.10')
        self.assertEqual(outdated[7]['current_version'], '2.4.8')
        self.assertEqual(outdated[7]['name'], 'openpyxl')
        self.assertEqual(outdated[7]['new_version'], '2.4.9')
        self.assertEqual(outdated[8]['current_version'], '3.0.1')
        self.assertEqual(outdated[8]['name'], 'pbr')
        self.assertEqual(outdated[8]['new_version'], '3.1.1')
        self.assertEqual(outdated[9]['current_version'], '0.4.0')
        self.assertEqual(outdated[9]['name'], 'pluggy')
        self.assertEqual(outdated[9]['new_version'], '0.5.2')
        self.assertEqual(outdated[10]['current_version'], '1.4.33')
        self.assertEqual(outdated[10]['name'], 'py')
        self.assertEqual(outdated[10]['new_version'], '1.5.2')
        self.assertEqual(outdated[11]['current_version'], '1.5.0')
        self.assertEqual(outdated[11]['name'], 'pyflakes')
        self.assertEqual(outdated[11]['new_version'], '1.6.0')
        self.assertEqual(outdated[12]['current_version'], '1.7.2')
        self.assertEqual(outdated[12]['name'], 'pylint')
        self.assertEqual(outdated[12]['new_version'], '1.7.4')
        self.assertEqual(outdated[13]['current_version'], '2.6.0')
        self.assertEqual(outdated[13]['name'], 'python-dateutil')
        self.assertEqual(outdated[13]['new_version'], '2.6.1')
        self.assertEqual(outdated[14]['current_version'], '2017.2')
        self.assertEqual(outdated[14]['name'], 'pytz')
        self.assertEqual(outdated[14]['new_version'], '2017.3')
        self.assertEqual(outdated[15]['current_version'], '2.0.2')
        self.assertEqual(outdated[15]['name'], 'radon')
        self.assertEqual(outdated[15]['new_version'], '2.1.1')
        self.assertEqual(outdated[16]['current_version'], '2.14.2')
        self.assertEqual(outdated[16]['name'], 'requests')
        self.assertEqual(outdated[16]['new_version'], '2.18.4')
        self.assertEqual(outdated[17]['current_version'], '36.0.1')
        self.assertEqual(outdated[17]['name'], 'setuptools')
        self.assertEqual(outdated[17]['new_version'], '37.0.0')
        self.assertEqual(outdated[18]['current_version'], '1.10.0')
        self.assertEqual(outdated[18]['name'], 'six')
        self.assertEqual(outdated[18]['new_version'], '1.11.0')
        self.assertEqual(outdated[19]['current_version'], '2.7.0')
        self.assertEqual(outdated[19]['name'], 'tox')
        self.assertEqual(outdated[19]['new_version'], '2.9.1')
        self.assertEqual(outdated[20]['current_version'], '1.10.10')
        self.assertEqual(outdated[20]['name'], 'wrapt')
        self.assertEqual(outdated[20]['new_version'], '1.10.11')

    def test_list_libraries(self):
        outdated = list_libraries()
        self.assertTrue(len(outdated)> 10)



class TestReadRequirementFile(TestFixtureMixin, SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestReadRequirementFile, cls).setUpClass()
        cls.pip_main_result = b'Django (1.11.3) - Latest: 2.1.0 [wheel]\ncelery (4.0.1) - Latest: 4.10.1 [wheel]\n' \
                      b'cookiecutter (1.5.1) - Latest: 1.6.0 [wheel]\ncoverage (4.4.1) - Latest: 4.4.2 [wheel]\n' \
                      b'Faker (0.7.17) - Latest: 0.8.7 [wheel]\nflake8 (3.3.0) - Latest: 3.5.0 [wheel]\n' \
                      b'Jinja2 (2.9.6) - Latest: 2.10 [wheel]\nopenpyxl (2.4.8) - Latest: 2.4.9 [sdist]\n' \
                      b'pbr (3.0.1) - Latest: 3.1.1 [wheel]\npluggy (0.4.0) - Latest: 0.5.2 [sdist]\n' \
                      b'py (1.4.33) - Latest: 1.5.2 [wheel]\npyflakes (1.5.0) - Latest: 1.6.0 [wheel]\n' \
                      b'pylint (1.7.2) - Latest: 1.7.4 [wheel]\npython-dateutil (2.6.0) - Latest: 2.6.1 [wheel]\n' \
                      b'pytz (2017.2) - Latest: 2017.3 [wheel]\nradon (2.0.2) - Latest: 2.1.1 [wheel]\n' \
                      b'requests (2.14.2) - Latest: 2.18.4 [wheel]\nsetuptools (36.0.1) - Latest: 37.0.0 [wheel]\n' \
                      b'six (1.10.0) - Latest: 1.11.0 [wheel]\ntox (2.7.0) - Latest: 2.9.1 [wheel]\n' \
                      b'wrapt (1.10.10) - Latest: 1.10.11 [sdist]\n' \
                      b'DEPRECATION: The default format will switch to columns in the future. ' \
                      b'You can use --format=(legacy|columns) (or define a format=(legacy|columns) in your pip.conf ' \
                      b'under the [list] section) to disable this warning.\n'

    def setUp(self):
        self.requirements = list()
        self.requirements.append('django==1.11.3 # pyup: >=1.10,<1.11\n')
        self.requirements.append('celery==4.0.1\n')
        self.requirements.append('redis>=2.10.5\n')

    @mock.patch('django_test_tools.pip.utils.pip._internal.main')
    @temporary_file(extension='txt', delete_on_exit=True)
    def test_update_outdated_libraries(self, mock_pip_main):
        filename = self.test_update_outdated_libraries.filename
        with open(filename, 'w', encoding='utf-8') as req_file:
            req_file.writelines(self.requirements)

        mock_capture = mock.Mock()
        mock_capture.return_value = self.pip_main_result

        with mock.patch('django_test_tools.pip.utils.subprocess.check_output', mock_capture):
            changes = update_outdated_libraries(filename)
        #write_assertions(changes, 'changes')

        #mock_pip_main.assert_called_with(['list', '--outdated'])
        self.assertEqual(len(changes), 2)
        self.assertIsNotNone(changes[0]['filename'])
        self.assertEqual(changes[0]['library_name'], 'django')
        self.assertEqual(changes[0]['line_no'], 0)
        self.assertEqual(changes[0]['new'], 'django==2.1.0')
        self.assertEqual(changes[0]['previous'], 'django==1.11.3 # pyup: >=1.10,<1.11')
        self.assertIsNotNone(changes[1]['filename'])
        self.assertEqual(changes[1]['library_name'], 'celery')
        self.assertEqual(changes[1]['line_no'], 1)
        self.assertEqual(changes[1]['new'], 'celery==4.10.1')
        self.assertEqual(changes[1]['previous'], 'celery==4.0.1')

    @temporary_file(extension='txt', delete_on_exit=True)
    def test_read_requirement_file(self):
        filename = self.test_read_requirement_file.filename

        with open(filename, 'w', encoding='utf-8') as req_file:
            req_file.writelines(self.requirements)

        requirements = read_requirement_file(filename)
        # write_assertions(requirements, 'requirements')
        self.assertEqual(requirements['celery']['comes_from']['file_indicator'], '-r')
        self.assertTrue(filename in requirements['celery']['comes_from']['filename'])
        self.assertEqual(requirements['celery']['comes_from']['line_no'], 2)
        self.assertTrue(filename in requirements['celery']['comes_from']['value'])
        self.assertEqual(requirements['celery']['name'], 'celery')
        self.assertEqual(requirements['celery']['operator'], '==')
        self.assertEqual(requirements['celery']['version'], '4.0.1')
        self.assertEqual(requirements['django']['comes_from']['file_indicator'], '-r')
        self.assertTrue(filename in requirements['django']['comes_from']['filename'])
        self.assertEqual(requirements['django']['comes_from']['line_no'], 1)
        self.assertTrue(filename in requirements['django']['comes_from']['value'])
        self.assertEqual(requirements['django']['name'], 'django')
        self.assertEqual(requirements['django']['operator'], '==')
        self.assertEqual(requirements['django']['version'], '1.11.3')
        self.assertEqual(requirements['redis']['comes_from']['file_indicator'], '-r')
        self.assertTrue(filename in requirements['redis']['comes_from']['filename'])
        self.assertEqual(requirements['redis']['comes_from']['line_no'], 3)
        self.assertTrue(filename in requirements['redis']['comes_from']['value'])
        self.assertEqual(requirements['redis']['name'], 'redis')
        self.assertEqual(requirements['redis']['operator'], '>=')
        self.assertEqual(requirements['redis']['version'], '2.10.5')

    @mock.patch('django_test_tools.pip.utils.requests.get')
    def test_get_latest_version(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.get_json_data('celery.json')
        mock_get.return_value = mock_response
        version = get_latest_version('celery')
        self.assertEqual(version, '4.1.0')
        mock_get.assert_called_with('https://pypi.python.org/pypi/celery/json')
