import datetime
import logging
import os
from unittest import mock

from django.test import TestCase, SimpleTestCase

from django_test_tools.file_utils import TemporaryFolder, hash_file
from django_test_tools.utils import Timer, spanish_date_util, \
    dict_compare, convert_to_snake_case, datetime_to_local_time

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
            # clock.increment(3600.0)
            stopwatch = Timer()
            stopwatch.start()
            clock.increment(120.5)
            stopwatch.stop()
            self.assertEqual('0 h 2 m 0.50 s', stopwatch.get_elapsed_time_str())

    def test_get_elapsed_time_str_with(self):
        clock = MockPerfCounter()
        with mock.patch('time.perf_counter', clock.perf_counter):
            # clock.increment(3600.0)
            with Timer() as stopwatch:
                clock.increment(360.25)
            self.assertEqual('0 h 6 m 0.25 s', stopwatch.get_elapsed_time_str())


class TestSpanishDate(TestCase):
    def test_to_string(self):
        start_date = datetime.date(2016, 12, 3)
        str_date = spanish_date_util.to_string(start_date)
        self.assertEqual('03-Dic-16', str_date)

    def test_to_string_datetime(self):
        start_date = datetime.datetime(2016, 12, 3, 16, 15)
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


class TestSnakeCase(SimpleTestCase):

    def test_convert_to_snake_case(self):
        camel_case = 'OperatingSystem'
        snake_case = convert_to_snake_case(camel_case)
        self.assertEqual(snake_case, 'operating_system')

    def test_convert_to_snake_case_long(self):
        camel_case = 'OperatingSystemLongName'
        snake_case = convert_to_snake_case(camel_case)
        self.assertEqual(snake_case, 'operating_system_long_name')


class TestDatetimeToLocalTime(SimpleTestCase):

    def test_datetime_to_local_time_datetime(self):
        input_date_format = '%Y-%m-%d %H:%M:%S %z'
        output_date_format = '%Y-%m-%d %H:%M:%S'
        date_value = '2018-09-23 09:37:50 -0500'
        datetime_object = datetime.datetime.strptime(date_value, input_date_format)

        datetime_object_with_timezone = datetime_to_local_time(datetime_object)
        str_datetime_w_tz = datetime_object_with_timezone.strftime(output_date_format)
        self.assertEqual(str_datetime_w_tz, '2018-09-23 09:37:50')

    def test_datetime_to_local_time_date(self):
        input_date_format = '%Y-%m-%d %H:%M:%S %z'
        output_date_format = '%Y-%m-%d %H:%M:%S'
        date_value = '2018-09-23 09:37:50 -0500'
        date_object = datetime.datetime.strptime(date_value, input_date_format).date()

        datetime_object_with_timezone = datetime_to_local_time(date_object)
        str_datetime_w_tz = datetime_object_with_timezone.strftime(output_date_format)
        self.assertEqual(str_datetime_w_tz, '2018-09-23 00:00:00')
