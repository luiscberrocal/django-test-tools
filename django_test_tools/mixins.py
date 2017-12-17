import csv
import os
from io import StringIO

from .excel import ExcelAdapter


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
