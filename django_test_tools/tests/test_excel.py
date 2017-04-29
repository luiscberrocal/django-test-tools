from django.test import TestCase
from openpyxl import Workbook
import os
from ..excel import ExcelAdapter
from django.conf import settings
from ..utils import  add_date_to_filename, create_output_filename_with_date
from faker import Factory as FakerFactory

faker = FakerFactory.create()

class TestExcelAdapter(TestCase):

    clean_output = True

    def setUp(self):
        self.filename = create_output_filename_with_date('excel_test_.xlsx')
        wb = Workbook()
        sheet = wb.active
        self.sheet_name ='My New Sheet'
        sheet.title = self.sheet_name
        for row in range(0, 10):
            for column in range(0, 5):
                sheet.cell(column=column+1, row=row+1, value=faker.word())
        wb.save(self.filename)

    def test_convert_to_list(self):
        adapter = ExcelAdapter()
        data = adapter.convert_to_list(self.filename, self.sheet_name)
        self.assertEqual(9, len(data))
        self.assertEqual(5, len(data[0]))
        if self.clean_output:
            os.remove(self.filename)
            self.assertFalse(os.path.exists(self.filename))

