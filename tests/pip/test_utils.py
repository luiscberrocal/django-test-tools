from django.test import SimpleTestCase
import re
from django_test_tools.pip.utils import list_libraries, parse_pip_list


class TestCaselist_libraries(SimpleTestCase):

    # def test_list_libraries(self):
    #     libraries = list_libraries()
    #     django_found = False
    #     django_test_tools_found = False
    #     version_regexp = re.compile(r'\d+\.\d+\.\d+')
    #     for library in libraries:
    #         if library.get('name') == 'django':
    #             django_found = True
    #             match = version_regexp.match(library.get('current_version'))
    #             self.assertTrue(match is not None)
    #         if library.get('name') == 'django-test-tools':
    #             django_test_tools_found = True
    #             match = version_regexp.match(library.get('current_version'))
    #             self.assertTrue(match is not None)
    #     self.assertTrue(django_found)
    #     self.assertTrue(django_test_tools_found)

    def test_list_libraries_outdated(self):
        libraries = list_libraries(outdated=True)
        django_found = False
        django_test_tools_found = False
        version_regexp = re.compile(r'\d+\.\d+\.\d+')
        for library in libraries:
            if library.get('name') == 'django':
                django_found = True
                match = version_regexp.match(library.get('current_version'))
                self.assertTrue(match is not None)


class Testparse_pip_list(SimpleTestCase):

    def test_parse_pip_list(self):
        lines = list()
        lines.append('asn1crypto        0.24.0    1.3.0      wheel')
        lines.append('bleach            3.0.2     3.1.3      wheel')
        version_regexp = re.compile(r'\d+\.\d+\.\d+')
        for line in lines:
            result = parse_pip_list(line)
            self.assertTrue(result['name'] in ['asn1crypto', 'bleach'])
            match = version_regexp.match(result.get('current_version'))
            self.assertTrue(match is not None)
            match = version_regexp.match(result.get('new_version'))
            self.assertTrue(match is not None)
