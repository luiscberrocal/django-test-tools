from django.conf import settings
from django.test import SimpleTestCase

from django_test_tools.assert_utils import write_assertions
from django_test_tools.pip.utils import parse_specifier, read_requirement_file


class TestParseSpecifier(SimpleTestCase):

    def test_parse_specifier(self):
        result = parse_specifier('==2.1.1')
        self.assertEqual(result[0], '==')
        self.assertEqual(result[1], '2.1.1')

    def test_parse_specifier(self):
        with self.assertRaises(ValueError) as context:
            parse_specifier('2.1.1')

        self.assertEqual(str(context.exception), 'Invalid speficier "2.1.1"')


class TestReadRequirementFile(SimpleTestCase):

    def test_read_requirement_file(self):
        filename = settings.ROOT_DIR.path('tests', 'fixtures', 'local.txt').root
        requirements = read_requirement_file(filename)
        #write_assertions(requirements, 'requirements')
        self.assertEqual(len(requirements), 42)
        self.assertEqual(requirements[0]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[0]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[0]['comes_from']['line_no'], '5')
        self.assertEqual(requirements[0]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 5)')
        self.assertEqual(requirements[0]['name'], 'wheel')
        self.assertEqual(requirements[0]['operator'], '==')
        self.assertEqual(requirements[0]['version'], '0.29.0')
        self.assertEqual(requirements[1]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[1]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[1]['comes_from']['line_no'], '8')
        self.assertEqual(requirements[1]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 8)')
        self.assertEqual(requirements[1]['name'], 'django')
        self.assertEqual(requirements[1]['operator'], '==')
        self.assertEqual(requirements[1]['version'], '1.11.7')
        self.assertEqual(requirements[2]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[2]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[2]['comes_from']['line_no'], '11')
        self.assertEqual(requirements[2]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 11)')
        self.assertEqual(requirements[2]['name'], 'django-environ')
        self.assertEqual(requirements[2]['operator'], '==')
        self.assertEqual(requirements[2]['version'], '0.4.4')
        self.assertEqual(requirements[3]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[3]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[3]['comes_from']['line_no'], '15')
        self.assertEqual(requirements[3]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 15)')
        self.assertEqual(requirements[3]['name'], 'django-braces')
        self.assertEqual(requirements[3]['operator'], '==')
        self.assertEqual(requirements[3]['version'], '1.11.0')
        self.assertEqual(requirements[4]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[4]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[4]['comes_from']['line_no'], '16')
        self.assertEqual(requirements[4]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 16)')
        self.assertEqual(requirements[4]['name'], 'django-crispy-forms')
        self.assertEqual(requirements[4]['operator'], '==')
        self.assertEqual(requirements[4]['version'], '1.6.1')
        self.assertEqual(requirements[5]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[5]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[5]['comes_from']['line_no'], '17')
        self.assertEqual(requirements[5]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 17)')
        self.assertEqual(requirements[5]['name'], 'django-floppyforms')
        self.assertEqual(requirements[5]['operator'], '==')
        self.assertEqual(requirements[5]['version'], '1.7.0')
        self.assertEqual(requirements[6]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[6]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[6]['comes_from']['line_no'], '20')
        self.assertEqual(requirements[6]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 20)')
        self.assertEqual(requirements[6]['name'], 'django-model-utils')
        self.assertEqual(requirements[6]['operator'], '==')
        self.assertEqual(requirements[6]['version'], '3.0.0')
        self.assertEqual(requirements[7]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[7]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[7]['comes_from']['line_no'], '23')
        self.assertEqual(requirements[7]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 23)')
        self.assertEqual(requirements[7]['name'], 'Pillow')
        self.assertEqual(requirements[7]['operator'], '==')
        self.assertEqual(requirements[7]['version'], '4.3.0')
        self.assertEqual(requirements[8]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[8]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[8]['comes_from']['line_no'], '28')
        self.assertEqual(requirements[8]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 28)')
        self.assertEqual(requirements[8]['name'], 'psycopg2')
        self.assertEqual(requirements[8]['operator'], '==')
        self.assertEqual(requirements[8]['version'], '2.7.3.1')
        self.assertEqual(requirements[9]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[9]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[9]['comes_from']['line_no'], '31')
        self.assertEqual(requirements[9]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 31)')
        self.assertEqual(requirements[9]['name'], 'unicode-slugify')
        self.assertEqual(requirements[9]['operator'], '==')
        self.assertEqual(requirements[9]['version'], '0.1.3')
        self.assertEqual(requirements[10]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[10]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[10]['comes_from']['line_no'], '32')
        self.assertEqual(requirements[10]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 32)')
        self.assertEqual(requirements[10]['name'], 'django-autoslug')
        self.assertEqual(requirements[10]['operator'], '==')
        self.assertEqual(requirements[10]['version'], '1.9.3')
        self.assertEqual(requirements[11]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[11]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[11]['comes_from']['line_no'], '37')
        self.assertEqual(requirements[11]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 37)')
        self.assertEqual(requirements[11]['name'], 'pytz')
        self.assertEqual(requirements[11]['operator'], '==')
        self.assertEqual(requirements[11]['version'], '2017.2')
        self.assertEqual(requirements[12]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[12]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[12]['comes_from']['line_no'], '40')
        self.assertEqual(requirements[12]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 40)')
        self.assertEqual(requirements[12]['name'], 'django-redis')
        self.assertEqual(requirements[12]['operator'], '==')
        self.assertEqual(requirements[12]['version'], '4.8.0')
        self.assertEqual(requirements[13]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[13]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[13]['comes_from']['line_no'], '41')
        self.assertEqual(requirements[13]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 41)')
        self.assertEqual(requirements[13]['name'], 'redis')
        self.assertEqual(requirements[13]['operator'], '>=')
        self.assertEqual(requirements[13]['version'], '2.10.0')
        self.assertEqual(requirements[14]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[14]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[14]['comes_from']['line_no'], '44')
        self.assertEqual(requirements[14]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 44)')
        self.assertEqual(requirements[14]['name'], 'celery')
        self.assertEqual(requirements[14]['operator'], '==')
        self.assertEqual(requirements[14]['version'], '4.1.0')
        self.assertEqual(requirements[15]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[15]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[15]['comes_from']['line_no'], '47')
        self.assertEqual(requirements[15]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 47)')
        self.assertEqual(requirements[15]['name'], 'django-nose')
        self.assertEqual(requirements[15]['operator'], '==')
        self.assertEqual(requirements[15]['version'], '1.4.5')
        self.assertEqual(requirements[16]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[16]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[16]['comes_from']['line_no'], '53')
        self.assertEqual(requirements[16]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 53)')
        self.assertEqual(requirements[16]['name'], 'ldap3')
        self.assertEqual(requirements[16]['operator'], '==')
        self.assertEqual(requirements[16]['version'], '2.3')
        self.assertEqual(requirements[17]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[17]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[17]['comes_from']['line_no'], '55')
        self.assertEqual(requirements[17]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 55)')
        self.assertEqual(requirements[17]['name'], 'django-auth-ldap3-ad')
        self.assertEqual(requirements[17]['operator'], '==')
        self.assertEqual(requirements[17]['version'], '1.6.22')
        self.assertEqual(requirements[18]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[18]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[18]['comes_from']['line_no'], '57')
        self.assertEqual(requirements[18]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 57)')
        self.assertEqual(requirements[18]['name'], 'requests')
        self.assertEqual(requirements[18]['operator'], '==')
        self.assertEqual(requirements[18]['version'], '2.18.4')
        self.assertEqual(requirements[19]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[19]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[19]['comes_from']['line_no'], '58')
        self.assertEqual(requirements[19]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 58)')
        self.assertEqual(requirements[19]['name'], 'django-mptt')
        self.assertEqual(requirements[19]['operator'], '==')
        self.assertEqual(requirements[19]['version'], '0.8.7')
        self.assertEqual(requirements[20]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[20]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[20]['comes_from']['line_no'], '59')
        self.assertEqual(requirements[20]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 59)')
        self.assertEqual(requirements[20]['name'], 'openpyxl')
        self.assertEqual(requirements[20]['operator'], '==')
        self.assertEqual(requirements[20]['version'], '2.4.9')
        self.assertEqual(requirements[21]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[21]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[21]['comes_from']['line_no'], '60')
        self.assertEqual(requirements[21]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 60)')
        self.assertEqual(requirements[21]['name'], 'django-auditlog')
        self.assertEqual(requirements[21]['operator'], '==')
        self.assertEqual(requirements[21]['version'], '0.4.3')
        self.assertEqual(requirements[22]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[22]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[22]['comes_from']['line_no'], '61')
        self.assertEqual(requirements[22]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 61)')
        self.assertEqual(requirements[22]['name'], 'acp-calendar')
        self.assertEqual(requirements[22]['operator'], '==')
        self.assertEqual(requirements[22]['version'], '1.7.0')
        self.assertEqual(requirements[23]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[23]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[23]['comes_from']['line_no'], '62')
        self.assertEqual(requirements[23]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 62)')
        self.assertEqual(requirements[23]['name'], 'djangorestframework')
        self.assertEqual(requirements[23]['operator'], '==')
        self.assertEqual(requirements[23]['version'], '3.7.1')
        self.assertEqual(requirements[24]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[24]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[24]['comes_from']['line_no'], '63')
        self.assertEqual(requirements[24]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 63)')
        self.assertEqual(requirements[24]['name'], 'django-extensions')
        self.assertEqual(requirements[24]['operator'], '==')
        self.assertEqual(requirements[24]['version'], '1.9.0')
        self.assertEqual(requirements[25]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[25]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[25]['comes_from']['line_no'], '64')
        self.assertEqual(requirements[25]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 64)')
        self.assertEqual(requirements[25]['name'], 'django-import-export')
        self.assertEqual(requirements[25]['operator'], '==')
        self.assertEqual(requirements[25]['version'], '0.5.1')
        self.assertEqual(requirements[26]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[26]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[26]['comes_from']['line_no'], '65')
        self.assertEqual(requirements[26]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 65)')
        self.assertEqual(requirements[26]['name'], 'django-taggit')
        self.assertEqual(requirements[26]['operator'], '==')
        self.assertEqual(requirements[26]['version'], '0.22.1')
        self.assertEqual(requirements[27]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[27]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[27]['comes_from']['line_no'], '67')
        self.assertEqual(requirements[27]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 67)')
        self.assertEqual(requirements[27]['name'], 'django-guardian')
        self.assertEqual(requirements[27]['operator'], '==')
        self.assertEqual(requirements[27]['version'], '1.4.9')
        self.assertEqual(requirements[28]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[28]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt')
        self.assertEqual(requirements[28]['comes_from']['line_no'], '68')
        self.assertEqual(requirements[28]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/base.txt (line 68)')
        self.assertEqual(requirements[28]['name'], 'django-test-tools')
        self.assertEqual(requirements[28]['operator'], '==')
        self.assertEqual(requirements[28]['version'], '0.7.6')
        self.assertEqual(requirements[29]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[29]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[29]['comes_from']['line_no'], '3')
        self.assertEqual(requirements[29]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 3)')
        self.assertEqual(requirements[29]['name'], 'coverage')
        self.assertEqual(requirements[29]['operator'], '>=')
        self.assertEqual(requirements[29]['version'], '4.4.1')
        self.assertEqual(requirements[30]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[30]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[30]['comes_from']['line_no'], '4')
        self.assertEqual(requirements[30]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 4)')
        self.assertEqual(requirements[30]['name'], 'django-coverage-plugin')
        self.assertEqual(requirements[30]['operator'], '==')
        self.assertEqual(requirements[30]['version'], '1.5.0')
        self.assertEqual(requirements[31]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[31]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[31]['comes_from']['line_no'], '5')
        self.assertEqual(requirements[31]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 5)')
        self.assertEqual(requirements[31]['name'], 'Sphinx')
        self.assertEqual(requirements[31]['operator'], '==')
        self.assertEqual(requirements[31]['version'], '1.6.3')
        self.assertEqual(requirements[32]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[32]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[32]['comes_from']['line_no'], '7')
        self.assertEqual(requirements[32]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 7)')
        self.assertEqual(requirements[32]['name'], 'Werkzeug')
        self.assertEqual(requirements[32]['operator'], '==')
        self.assertEqual(requirements[32]['version'], '0.12.2')
        self.assertEqual(requirements[33]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[33]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[33]['comes_from']['line_no'], '8')
        self.assertEqual(requirements[33]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 8)')
        self.assertEqual(requirements[33]['name'], 'django-test-plus')
        self.assertEqual(requirements[33]['operator'], '==')
        self.assertEqual(requirements[33]['version'], '1.0.18')
        self.assertEqual(requirements[34]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[34]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[34]['comes_from']['line_no'], '9')
        self.assertEqual(requirements[34]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 9)')
        self.assertEqual(requirements[34]['name'], 'factory-boy')
        self.assertEqual(requirements[34]['operator'], '==')
        self.assertEqual(requirements[34]['version'], '2.9.2')
        self.assertEqual(requirements[35]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[35]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[35]['comes_from']['line_no'], '10')
        self.assertEqual(requirements[35]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 10)')
        self.assertEqual(requirements[35]['name'], 'bumpversion')
        self.assertEqual(requirements[35]['operator'], '==')
        self.assertEqual(requirements[35]['version'], '0.5.3')
        self.assertEqual(requirements[36]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[36]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[36]['comes_from']['line_no'], '12')
        self.assertEqual(requirements[36]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 12)')
        self.assertEqual(requirements[36]['name'], 'ipdb')
        self.assertEqual(requirements[36]['operator'], '==')
        self.assertEqual(requirements[36]['version'], '0.10.3')
        self.assertEqual(requirements[37]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[37]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[37]['comes_from']['line_no'], '14')
        self.assertEqual(requirements[37]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 14)')
        self.assertEqual(requirements[37]['name'], 'pytest-django')
        self.assertEqual(requirements[37]['operator'], '==')
        self.assertEqual(requirements[37]['version'], '3.1.2')
        self.assertEqual(requirements[38]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[38]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[38]['comes_from']['line_no'], '15')
        self.assertEqual(requirements[38]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 15)')
        self.assertEqual(requirements[38]['name'], 'pytest-sugar')
        self.assertEqual(requirements[38]['operator'], '==')
        self.assertEqual(requirements[38]['version'], '0.9.0')
        self.assertEqual(requirements[39]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[39]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[39]['comes_from']['line_no'], '16')
        self.assertEqual(requirements[39]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 16)')
        self.assertEqual(requirements[39]['name'], 'hypothesis')
        self.assertEqual(requirements[39]['operator'], '==')
        self.assertEqual(requirements[39]['version'], '3.24.0')
        self.assertEqual(requirements[40]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[40]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[40]['comes_from']['line_no'], '17')
        self.assertEqual(requirements[40]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 17)')
        self.assertEqual(requirements[40]['name'], 'django-debug-toolbar')
        self.assertEqual(requirements[40]['operator'], '==')
        self.assertEqual(requirements[40]['version'], '1.8')
        self.assertEqual(requirements[41]['comes_from']['file_indicator'], '-r')
        self.assertEqual(requirements[41]['comes_from']['filename'],
                         '/Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt')
        self.assertEqual(requirements[41]['comes_from']['line_no'], '20')
        self.assertEqual(requirements[41]['comes_from']['value'],
                         '-r /Users/lberrocal/PycharmProjects/django-test-tools/tests/fixtures/local.txt (line 20)')
        self.assertEqual(requirements[41]['name'], 'unittest-xml-reporting')
        self.assertEqual(requirements[41]['operator'], '==')
        self.assertEqual(requirements[41]['version'], '2.1.0')
