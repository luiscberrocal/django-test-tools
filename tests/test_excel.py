import json

from django.test import TestCase
from faker import Factory as FakerFactory
from openpyxl import Workbook

from django_test_tools.excel import ExcelAdapter
from django_test_tools.file_utils import temporary_file, hash_file

faker = FakerFactory.create()


class TestExcelAdapter(TestCase):
    clean_output = True

    def _create_file(self, filename, sheet_name=None):
        # self.filename = create_output_filename_with_date('excel_test3_.xlsx')
        wb = Workbook()
        sheet = wb.active
        if sheet_name is None:
            sheet_name = 'My New Sheet'
        sheet.title = sheet_name
        for row in range(0, 10):
            for column in range(0, 5):
                sheet.cell(column=column + 1, row=row + 1, value=faker.word())
        wb.save(filename)

    @temporary_file('.xlsx', delete_on_exit=True)
    def test_convert_to_list(self):
        sheet_name = 'MySheet'
        filename = self.test_convert_to_list.filename
        self._create_file(filename, sheet_name)
        adapter = ExcelAdapter()
        data = adapter.convert_to_list(filename, sheet_name)
        self.assertEqual(9, len(data))
        self.assertEqual(5, len(data[0]))

    @temporary_file('.json', delete_on_exit=True)
    def test_convert_to_dict(self):
        import environ
        full_path = (environ.Path(__file__) - 1).path('fixtures', 'excel_to_json.xlsx').root
        dict_data = ExcelAdapter.convert_to_dict(full_path)
        output = self.test_convert_to_dict.filename
        with open(output, 'w') as json_file:
            json.dump(dict_data, json_file)
        hash = hash_file(output)
        self.assertEqual(hash, '6ae7bfd81e52ace91f619e4b5586eb687888f43b')
