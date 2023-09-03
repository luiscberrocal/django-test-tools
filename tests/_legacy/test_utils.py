import datetime
from unittest import mock

import pytz
from django.test import TestCase, override_settings

from django_test_tools._legacy.utils import add_date_to_filename, create_output_filename_with_date, daterange
from django_test_tools.utils import parse_spanish_date


class TestAddDateToFilename(TestCase):
    def setUp(self):
        self.mock_datetime = pytz.timezone('America/Panama').localize(
            datetime.datetime.strptime('2016-07-07 16:40:39', '%Y-%m-%d %H:%M:%S'))

    @mock.patch('django.utils.timezone.now')
    def test_add_date_to_filename_suffix_path(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date_to_filename(filename)

        self.assertEquals(r'c:\kilo\poli\namos_20160707_1640.txt', new_filename)

        filename = r'c:\kilo\poli\namos.nemo.txt'
        new_filename = add_date_to_filename(filename)

        self.assertEquals(r'c:\kilo\poli\namos.nemo_20160707_1640.txt', new_filename)

        filename = r'/my/linux/path/namos.nemo.txt'
        new_filename = add_date_to_filename(filename)

        self.assertEquals(r'/my/linux/path/namos.nemo_20160707_1640.txt', new_filename)

    @mock.patch('os.path.exists')
    @mock.patch('django.utils.timezone.now')
    def test_add_date_to_filename_suffix_path_existing_file(self, mock_now, mock_exists):
        mock_now.return_value = self.mock_datetime
        mock_exists.return_value = True

        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date_to_filename(filename)

        self.assertEquals(r'c:\kilo\poli\namos_20160707_164039.txt', new_filename)

        filename = r'c:\kilo\poli\namos.nemo.txt'
        new_filename = add_date_to_filename(filename)
        self.assertEquals(r'c:\kilo\poli\namos.nemo_20160707_164039.txt', new_filename)

        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date_to_filename(filename, date_position='prefix')
        self.assertEquals(r'c:\kilo\poli\20160707_164039_namos.txt', new_filename)

        filename = r'/my/linux/path/namos.nemo.txt'
        new_filename = add_date_to_filename(filename)

        self.assertEquals(r'/my/linux/path/namos.nemo_20160707_164039.txt', new_filename)

    @mock.patch('django.utils.timezone.now')
    def test_add_date_to_filename_preffix_path(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date_to_filename(filename, date_position='prefix')
        self.assertEquals(r'c:\kilo\poli\20160707_1640_namos.txt', new_filename)

        filename = r'/my/linux/path/namos.txt'
        new_filename = add_date_to_filename(filename, date_position='prefix')
        self.assertEquals(r'/my/linux/path/20160707_1640_namos.txt', new_filename)

    @mock.patch('django.utils.timezone.now')
    def test_add_date_to_filename_suffix_filename(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'namos.txt'
        new_filename = add_date_to_filename(filename)
        self.assertEqual('namos_20160707_1640.txt', new_filename)

    @override_settings(TEST_OUTPUT_PATH=None)
    def test_create_output_filename_with_date_error(self):
        try:
            create_output_filename_with_date('kilo.txt')
            self.fail('Should have thrown value error')
        except ValueError as e:
            msg = 'You need a the variable TEST_OUTPUT_PATH in settings.' \
                  ' It should point to a folderfor temporary data to be written and reviewed.'
            self.assertEqual(msg, str(e))

    def test_daterange(self):
        start_date = datetime.date(2015, 9, 1)
        end_date = datetime.date(2015, 9, 30)
        work_days = 0
        for dt in daterange(start_date, end_date):
            work_days += 1
            # logger.debug('Date: %s' % dt.strftime('%m-%d %a'))
            # self.assertFalse(dt.weekday() not in set([5, 6]))
        self.assertEqual(22, work_days)

    def test_daterange_week(self):
        start_date = datetime.date(2016, 10, 3)  # Monday
        end_date = datetime.date(2016, 10, 7)  # Friday
        work_days = 0
        for dt in daterange(start_date, end_date):
            work_days += 1
        self.assertEqual(5, work_days)

    def test_daterange_week_2(self):
        start_date = datetime.date(2016, 10, 3)  # Monday
        end_date = datetime.date(2016, 10, 7)  # Friday
        days = list(daterange(start_date, end_date))
        self.assertEqual(5, len(days))

    def test_daterange_one_day(self):
        start_date = datetime.date(2016, 10, 3)  # Monday
        end_date = start_date
        days = list(daterange(start_date, end_date))
        self.assertEqual(1, len(days))

    def test_parse_spanish_date(self):
        start_date = datetime.date(2016, 12, 3)  # Monday
        result = parse_spanish_date('03-Dic-16')
        self.assertTrue(result, start_date)

    def test_parse_spanish_date_datetime(self):
        start_date = datetime.datetime(2016, 12, 3, 13, 50)  # Monday
        result = parse_spanish_date('03-Dic-16 13:50')
        self.assertTrue(result, start_date)
