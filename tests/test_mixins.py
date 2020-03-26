import csv

from django.test import TestCase, SimpleTestCase

from django_test_tools.file_utils import temporary_file
from django_test_tools.mixins import TestOutputMixin, TestCommandMixin, TestFixtureMixin


class TestTestOutputMixin(TestCase):
    @temporary_file('csv', delete_on_exit=True)
    def test_get_csv_content(self):
        outputfile = self.test_get_csv_content.filename
        with open(outputfile, 'w', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow(['Title 1', 'Title 2', 'Title 3', 'Title 4', 'Title 5'])
            for i in range(0, 6):
                csv_writer.writerow(['Data {0}'.format(i)] * 5)

        output_mixin = TestOutputMixin()
        data = output_mixin.get_csv_content(outputfile)
        self.assertEqual(7, len(data))
        self.assertEqual('Title 1', data[0][0])


class TestTestCommandMixin(SimpleTestCase):

    def test_(self):
        mixin = TestCommandMixin()
        mixin.setUp()
        mixin.content.write('Kilo\n')
        mixin.content.write('VIctor\n')
        results = mixin.get_results()
        self.assertEqual(len(results),2)


class TestTestFixtureMixin(SimpleTestCase):

    def test_(self):
        mixin = TestFixtureMixin(app_name=None, strict=False)
        celery_data = mixin.get_fixture_json('celery.json')
        self.assertEqual(len(celery_data), 2)
