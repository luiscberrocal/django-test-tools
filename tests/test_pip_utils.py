from django.conf import settings
from django.test import SimpleTestCase

from django_test_tools.assert_utils import write_assertions
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
        outdated = list_outdated_libraries()
        #write_assertions(outdated, 'outdated')
        self.assertTrue(len(outdated)>0)
        self.assertIsNotNone(outdated[0]['current_version'])
        self.assertIsNotNone(outdated[0]['name'])
        self.assertIsNotNone(outdated[0]['new_version'])


class TestReadRequirementFile(SimpleTestCase):

    def test_update_outdated_libraries(self):
        filename = settings.ROOT_DIR.path('tests', 'fixtures', 'local.txt').root
        update_outdated_libraries(filename)

    def test_read_requirement_file(self):
        filename = settings.ROOT_DIR.path('tests', 'fixtures', 'local.txt').root
        requirements = read_requirement_file(filename)
        write_assertions(requirements, 'requirements')

