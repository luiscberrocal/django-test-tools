import datetime
from unittest import mock
import os

import pytz
from django.test import TestCase

import logging

from django.test import override_settings

from django_test_tools.file_utils import TemporaryFolder, hash_file
from django_test_tools.utils import Timer, add_date_to_filename, daterange, parse_spanish_date, spanish_date_util, \
    create_output_filename_with_date, dict_compare

logger = logging.getLogger(__name__)
__author__ = 'lberrocal'


class MockPerfCounter(object):

    def __init__(self):
        self.t = 0

    def increment(self, n):
        self.t += n

    def perf_counter(self):
        return self.t

class Testdict_compare(TestCase):

    def test_dict_compare(self):
        dict1 = {'name': 'Luis', 'colors': ['red', 'blue', 'black']}
        dict2 = {'name': 'Luis', 'colors': ['red', 'blue', 'black']}
        added, removed, modified, same = dict_compare(dict1, dict2)
        self.assertEqual(0, len(added))
        self.assertEqual(0, len(removed))
        self.assertEqual(0, len(modified))
        self.assertEqual(2, len(same))

    def test_dict_compare_removed(self):
        dict1 = {'name': 'Luis', 'colors': ['red', 'blue', 'black']}
        dict2 = {'name': 'Luis', 'colors': ['red', 'blue', 'black'], 'type': 'human'}
        added, removed, modified, same = dict_compare(dict1, dict2)
        self.assertEqual(0, len(added))
        self.assertEqual({'type'}, removed)
        self.assertEqual(0, len(modified))
        self.assertEqual({'colors', 'name'}, same)

        added, removed, modified, same = dict_compare(dict2, dict1)
        self.assertEqual({'type'}, added)
        self.assertEqual(0, len(removed))
        self.assertEqual(0, len(modified))
        self.assertEqual({'colors', 'name'}, same)

        dict1 = {'name': 'Luis', 'colors': ['red', 'blue']}
        added, removed, modified, same = dict_compare(dict2, dict1)
        self.assertEqual({'type'}, added)
        self.assertEqual(0, len(removed))
        self.assertEqual({'colors': (['red', 'blue', 'black'], ['red', 'blue'])}, modified)
        self.assertEqual({'name'}, same)

class TestTimer(TestCase):


    def test_get_elapsed_time_str(self):
        clock = MockPerfCounter()
        with mock.patch('time.perf_counter', clock.perf_counter):
            #clock.increment(3600.0)
            stopwatch = Timer()
            stopwatch.start()
            clock.increment(120.5)
            stopwatch.stop()
            self.assertEqual('0 h 2 m 0.50 s', stopwatch.get_elapsed_time_str())

    def test_get_elapsed_time_str_with(self):
        clock = MockPerfCounter()
        with mock.patch('time.perf_counter', clock.perf_counter):
            #clock.increment(3600.0)
            with Timer() as stopwatch:
                clock.increment(360.25)
            self.assertEqual('0 h 6 m 0.25 s', stopwatch.get_elapsed_time_str())


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
            #logger.debug('Date: %s' % dt.strftime('%m-%d %a'))
            # self.assertFalse(dt.weekday() not in set([5, 6]))
        self.assertEqual(22, work_days)

    def test_daterange_week(self):
        start_date = datetime.date(2016, 10, 3) # Monday
        end_date = datetime.date(2016, 10, 7) # Friday
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


class TestSpanishDate(TestCase):

    def test_to_string(self):
        start_date = datetime.date(2016, 12, 3)
        str_date = spanish_date_util.to_string(start_date)
        self.assertEqual('03-Dic-16', str_date)

    def test_to_string_datetime(self):
        start_date = datetime.datetime(2016, 12, 3, 16,15)
        str_date = spanish_date_util.to_string(start_date)
        self.assertEqual('03-Dic-16 16:15', str_date)

    def test_parse(self):
        start_date = datetime.datetime(2016, 12, 3, 13, 50)
        result = spanish_date_util.parse('03-Dic-16 13:50')
        self.assertTrue(result, start_date)

    def test_parse_date(self):
        start_date = datetime.date(2016, 12, 3)
        o_date = spanish_date_util.parse('03-Dic-16')
        self.assertEqual(o_date, start_date)


class TemporyFolderTest(TestCase):

    def test_temporary_folder_write_list(self):
        with TemporaryFolder('my_temp_list', delete_on_exit=True) as folder:
            self.assertTrue(os.path.exists(folder.new_path))
            filename = folder.write('m.txt', ['kilo', 'boma'])
            digest = hash_file(filename)
            self.assertEqual('5585c5895705bb5fe8906a2fd93453af5ee643b5', digest)
        self.assertFalse(os.path.exists(folder.new_path))

    def test_temporary_folder_write_str(self):
        with TemporaryFolder('my_temp_str') as folder:
            self.assertTrue(os.path.exists(folder.new_path))
            filename = folder.write('m.txt', 'Hola')
            digest = hash_file(filename)
            self.assertEqual('4e46dc0969e6621f2d61d2228e3cd91b75cd9edc', digest)
        self.assertFalse(os.path.exists(folder.new_path))

    def test_temporary_folder_write_other(self):
        with TemporaryFolder('my_temp_date') as folder:
            self.assertTrue(os.path.exists(folder.new_path))
            filename = folder.write('m.txt', datetime.date(2016, 12, 3))
            digest = hash_file(filename)
            self.assertEqual('2b7db434f52eb470e1a6dcdc39063536c075a4f0', digest)
        self.assertFalse(os.path.exists(folder.new_path))
