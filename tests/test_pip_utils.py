from unittest import mock

from django.test import SimpleTestCase

from django_test_tools.assert_utils import write_assertions
from django_test_tools.file_utils import temporary_file
from django_test_tools.pip.utils import parse_specifier, read_requirement_file, list_outdated_libraries, \
    update_outdated_libraries


class TestParseSpecifier(SimpleTestCase):
    def test_parse_specifier(self):
        result = parse_specifier('==2.1.1')
        self.assertEqual(result[0], '==')
        self.assertEqual(result[1], '2.1.1')

    def test_parse_specifier(self):
        with self.assertRaises(ValueError) as context:
            parse_specifier('2.1.1')

        self.assertEqual(str(context.exception), 'Invalid speficier "2.1.1"')


    def test_list_outdated_libraries(self):
        main_result = ['binaryornot (0.4.3) - Latest: 1.4.4 [wheel]\nchardet (3.0.2) - Latest: 3.0.4 [wheel]\n'
                       'cookiecutter (1.5.1) - Latest: 1.6.0 [wheel]\ncoverage (4.4.1) - Latest: 4.4.2 [wheel]\n'
                       'Faker (0.7.17) - Latest: 0.8.7 [wheel]\nflake8 (3.3.0) - Latest: 3.5.0 [wheel]\n'
                       'Jinja2 (2.9.6) - Latest: 2.10 [wheel]\nopenpyxl (2.4.8) - Latest: 2.4.9 [sdist]\n'
                       'pbr (3.0.1) - Latest: 3.1.1 [wheel]\npluggy (0.4.0) - Latest: 0.5.2 [sdist]\n'
                       'py (1.4.33) - Latest: 1.5.2 [wheel]\npyflakes (1.5.0) - Latest: 1.6.0 [wheel]\n'
                       'pylint (1.7.2) - Latest: 1.7.4 [wheel]\npython-dateutil (2.6.0) - Latest: 2.6.1 [wheel]\n'
                       'pytz (2017.2) - Latest: 2017.3 [wheel]\nradon (2.0.2) - Latest: 2.1.1 [wheel]\n'
                       'requests (2.14.2) - Latest: 2.18.4 [wheel]\nsetuptools (36.0.1) - Latest: 37.0.0 [wheel]\n'
                       'six (1.10.0) - Latest: 1.11.0 [wheel]\ntox (2.7.0) - Latest: 2.9.1 [wheel]\n'
                       'wrapt (1.10.10) - Latest: 1.10.11 [sdist]\n',
                       'DEPRECATION: The default format will switch to columns in the future. '
                       'You can use --format=(legacy|columns) (or define a format=(legacy|columns) in your pip.conf '
                       'under the [list] section) to disable this warning.\n']

        mock_capture = mock.Mock()
        mock_capture.return_value = mock_capture
        mock_capture.__enter__ = mock.Mock(return_value=('cookiecutter (1.5.1) - Latest: 1.6.0 [wheel]\n', ['\n']))
        mock_capture.__exit__ = mock.Mock(return_value=(mock.Mock(), None))

        #mock_capture.__exit__().return_value = ['cookiecutter (1.5.1) - Latest: 1.6.0 [wheel]\n'], ['\n']

        with mock.patch('django_test_tools.pip.utils.capture', mock_capture):
            outdated = list_outdated_libraries()
        #mock_pip_main.assert_called_with(['list', '--outdated'])
        write_assertions(outdated, 'outdated')
        self.fail('KILO')


    def test_list_outdated_libraries2(self):
        outdated = list_outdated_libraries()


class TestReadRequirementFile(SimpleTestCase):
    def setUp(self):
        self.requirements = list()
        self.requirements.append('django==1.11.3 # pyup: >=1.10,<1.11\n')
        self.requirements.append('celery==4.0.1\n')
        self.requirements.append('redis>=2.10.5\n')

    @temporary_file(extension='txt', delete_on_exit=False)
    def test_update_outdated_libraries(self):
        filename = self.test_update_outdated_libraries.filename
        with open(filename, 'w', encoding='utf-8') as req_file:
            req_file.writelines(self.requirements)
        changes = update_outdated_libraries(filename)
        write_assertions(changes, 'changes')
        self.fail('kkkk')

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
