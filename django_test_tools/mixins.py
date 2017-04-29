from io import StringIO
import os

from .excel import ExcelAdapter


class TestCommandMixin(object):

    def setUp(self):
        self.content = StringIO()



    def get_results(self, content=None):
        if content is None:
            content = self.content
        content.seek(0)
        lines = content.readlines()
        results = list()
        for line in lines:
            results.append(line.strip('\n'))
        return results

class TestOutputMixin(object):
    clean_output = True

    def clean_output_folder(self, dated_filename):
        if self.clean_output:
            os.remove(dated_filename)
            self.assertFalse(os.path.exists(dated_filename))

    def get_excel_content(self, filename, sheet_name=None):
        adapter = ExcelAdapter()
        return adapter.convert_to_list(filename, sheet_name)
