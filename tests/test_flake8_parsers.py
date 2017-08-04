from django.test import TestCase

from django_test_tools.assert_utils import write_assert_list
from django_test_tools.file_utils import temporary_file, create_dated, hash_file
from django_test_tools.flake8.parsers import Flake8Parser, RadonParser
from django_test_tools.mixins import TestOutputMixin


class Flake8ParserTest(TestOutputMixin, TestCase):

    def setUp(self):
        self.content = """
3     E124 closing bracket does not match visual indentation
6     E127 continuation line over-indented for visual indent
11    E128 continuation line under-indented for visual indent
2     E221 multiple spaces before operator
1     E222 multiple spaces after operator
10    E225 missing whitespace around operator
6     E231 missing whitespace after ','
2     E251 unexpected spaces around keyword / parameter equals
4     E261 at least two spaces before inline comment
4     E262 inline comment should start with '# '
8     E265 block comment should start with '# '
4     E266 too many leading '#' for block comment
2     E271 multiple spaces after keyword
5     E302 expected 2 blank lines, found 1
7     E303 too many blank lines (3)
2     E402 module level import not at top of file
8     E501 line too long (123 > 120 characters)
17    F401 'django.contrib.admin' imported but unused
25    F405 'env' may be undefined, or defined from star imports: .base
1     F811 redefinition of unused 'RemarksManager' from line 3
7     F841 local variable 'response' is assigned to but never used
2     W293 blank line contains whitespace
6     W391 blank line at end of file"""

    @temporary_file('txt')
    def test_parse_summary(self):
        parser = Flake8Parser()
        filename = self.test_parse_summary.filename
        with open(filename, 'w', encoding='utf-8') as pep8_file:
            pep8_file.write(self.content)
        summary = parser.parse_summary(filename)
        self.assertEqual(23, len(summary))

    @temporary_file('txt')
    def test_write_summary(self):
        parser = Flake8Parser()
        filename = self.test_write_summary.filename
        with open(filename, 'w', encoding='utf-8') as pep8_file:
            pep8_file.write(self.content)

        out_filename = create_dated('pep8_violations.csv')
        parser.write_summary(filename, out_filename)
        digest = hash_file(out_filename)
        self.assertEqual('20f5184854bd10ed0998c8e9029175ed08b097e0', digest)
        self.clean_output_folder(out_filename)

class RadonParserTest(TestOutputMixin, TestCase):

    def setUp(self):
        content = """
            config/settings/test.py
                LOC: 61
                LLOC: 12
                SLOC: 23
                Comments: 23
                Single comments: 22
                Multi: 4
                Blank: 12
                - Comment Stats
                    (C % L): 38%
                    (C % S): 100%
                    (C + M % L): 44%
            ** Total **
                LOC: 2149
                LLOC: 894
                SLOC: 1311
                Comments: 335
                Single comments: 310
                Multi: 128
                Blank: 400
                - Comment Stats
                    (C % L): 16%
                    (C % S): 26%
                    (C + M % L): 22%
            """
        self.filename = create_dated('radon.txt')
        with open(self.filename, 'w', encoding='utf-8') as radon_file:
            radon_file.write(content)


    def test_parse_totals(self):
        parser = RadonParser()
        results = parser.parse_totals(self.filename)
        #write_assert_list(None, results, 'results')

        self.assertEqual(400, results['blank'])
        self.assertEqual(335, results['comments'])
        self.assertEqual(894, results['lloc'])
        self.assertEqual(2149, results['loc'])
        self.assertEqual(128, results['multi'])
        self.assertEqual(310, results['single_comments'])
        self.assertEqual(1311, results['sloc'])
        self.clean_output_folder(self.filename)

    @temporary_file('csv', delete_on_exit=True)
    def test_write_totals(self):
        parser = RadonParser()
        parser.write_totals(self.filename, self.test_write_totals.filename)
        digest = hash_file(self.test_write_totals.filename)
        self.assertEqual('cc1ff3f88b894cf807e8fc755dfb26c3806bb41c', digest)
        self.clean_output_folder(self.filename)
