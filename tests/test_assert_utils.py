import logging
from datetime import datetime, date
from decimal import Decimal

import pytz
from django.test import TestCase, SimpleTestCase

from django_test_tools.assert_utils import write_assert_list, AssertionWriter, write_assertions
from django_test_tools.file_utils import temporary_file, hash_file
from django_test_tools.mixins import TestOutputMixin

logger = logging.getLogger(__name__)


class TestAssertionWriter(TestOutputMixin, SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestAssertionWriter, cls).setUpClass()
        cls.writer = AssertionWriter()

    def test_generate_assert_equals_dictionaries(self):
        data = [
            {'name': 'kilo', 'password': 9999, 'groups': ['admin', 'users']}
        ]

        results = self.writer._generate_assert_equals_list(data, 'data')
        self.assertEqual(results[0], 'self.assertEqual(len(data), 1)')

    @temporary_file('py', delete_on_exit=True)
    def test_write_assertions(self):
        data = [
            {'name': 'kilo', 'password': 9999,
             'groups': ['admin', 'users'],
             'config': {'server': 'all', 'bulding': 116}},
            {'name': 'pasto', 'password': 'nogo',
             'groups': ['users'],
             'config': {'server': 'database', 'bulding': 116},
             'created': '2016-10-01',
             'modified': '2016-10-01'}
        ]
        filename = write_assertions(data,
                                    'data', filename=self.test_write_assertions.filename,
                                    excluded_keys=['config'])
        self.assertEqual(filename, self.test_write_assertions.filename)
        hash_digest = hash_file(filename)
        self.assertEqual(hash_digest, 'bd059f11bb7a5a2db70c89d94c9cd681f4684fa4')
        content = self.get_txt_content(filename)

        self.assertEqual(len(content), 10)
        self.assertEqual(content[0], 'self.assertEqual(len(data), 2)')
        self.assertEqual(content[1], 'self.assertEqual(len(data[0][\'groups\']), 2)')
        self.assertEqual(content[2], 'self.assertEqual(data[0][\'groups\'][0], \'admin\')')
        self.assertEqual(content[3], 'self.assertEqual(data[0][\'groups\'][1], \'users\')')
        self.assertEqual(content[4], 'self.assertEqual(data[0][\'name\'], \'kilo\')')
        self.assertEqual(content[5], 'self.assertEqual(data[0][\'password\'], 9999)')
        self.assertEqual(content[6], 'self.assertEqual(len(data[1][\'groups\']), 1)')
        self.assertEqual(content[7], 'self.assertEqual(data[1][\'groups\'][0], \'users\')')
        self.assertEqual(content[8], 'self.assertEqual(data[1][\'name\'], \'pasto\')')
        self.assertEqual(content[9], 'self.assertEqual(data[1][\'password\'], \'nogo\')')

    @temporary_file('py', delete_on_exit=False)
    def test_write_assertions_type_only(self):
        data = [
            {'name': 'kilo', 'password': 9999,
             'groups': ['admin', 'users'],
             'config': {'server': 'all', 'bulding': 116}},
            {'name': 'pasto', 'password': 'nogo',
             'groups': ['users'],
             'config': {'server': 'database', 'bulding': None},
             'created_date': date(2016, 1, 3),
             'modified': '2016-10-01'}
        ]
        filename = write_assertions(data,
                                    'data', filename=self.test_write_assertions_type_only.filename,
                                    type_only=True)

        self.assertEqual(filename, self.test_write_assertions_type_only.filename)
        hash_digest = hash_file(filename)
        self.assertEqual(hash_digest, '702040e388cc1beebd865e6abc07b1ec1855296a')
        content = self.get_txt_content(filename)
        self.assertEqual(len(content), 15)
        self.assertEqual(content[0], 'self.assertEqual(len(data), 2)')
        self.assertEqual(content[1], 'self.assertIsNotNone(data[0][\'config\'][\'bulding\']) # Example: 116')
        self.assertEqual(content[2], 'self.assertIsNotNone(data[0][\'config\'][\'server\']) # Example: all')
        self.assertEqual(content[3], 'self.assertEqual(len(data[0][\'groups\']), 2)')
        self.assertEqual(content[4], 'self.assertIsNotNone(data[0][\'groups\'][0]) # Example: admin')
        self.assertEqual(content[5], 'self.assertIsNotNone(data[0][\'groups\'][1]) # Example: users')
        self.assertEqual(content[6], 'self.assertIsNotNone(data[0][\'name\']) # Example: kilo')
        self.assertEqual(content[7], 'self.assertIsNotNone(data[0][\'password\']) # Example: 9999')
        self.assertEqual(content[8], 'self.assertIsNone(data[1][\'config\'][\'bulding\']) # Example: None')
        self.assertEqual(content[9], 'self.assertIsNotNone(data[1][\'config\'][\'server\']) # Example: database')
        self.assertEqual(content[10],
                         'self.assertRegex(data[1][\'created_date\'].strftime(\'%Y-%m-%d\'), r\'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))\') # Example: 2016-01-03')
        self.assertEqual(content[11], 'self.assertEqual(len(data[1][\'groups\']), 1)')
        self.assertEqual(content[12], 'self.assertIsNotNone(data[1][\'groups\'][0]) # Example: users')
        self.assertEqual(content[13], 'self.assertIsNotNone(data[1][\'name\']) # Example: pasto')
        self.assertEqual(content[14], 'self.assertIsNotNone(data[1][\'password\']) # Example: nogo')

    @temporary_file('py', delete_on_exit=True)
    def test_write_assert_list(self):
        data = [
            {'name': 'kilo', 'password': 9999,
             'groups': ['admin', 'users'],
             'config': {'server': 'all', 'bulding': 116}},
            {'name': 'pasto', 'password': 'nogo',
             'groups': ['users'],
             'config': {'server': 'database', 'bulding': 116},
             'created': '2016-10-01',
             'modified': '2016-10-01'}
        ]
        filename = write_assert_list(self.test_write_assert_list.filename, data, 'data')
        self.assertEqual(filename, self.test_write_assert_list.filename)
        hash_digest = hash_file(filename)
        self.assertEqual('5cd2e29830c5c0a9af1e60a8f08b3ffc49cf92fb', hash_digest)

    @temporary_file('py', delete_on_exit=True)
    def test_write_assert_regexp(self):
        data = [
            {'name': 'kilo', 'password': 9999,
             'groups': ['ADMIN', 'USERS'],
             'config': {'server': 'all', 'bulding': 116}},
            {'name': 'pasto', 'password': 'nogo',
             'groups': ['users'],
             'config': {'server': 'database', 'bulding': 116},
             'time': '11:45',
             'cost': '1234.45',
             'created': '2016-10-01',
             'modified': '2016-10-01'}
        ]
        filename = self.test_write_assert_regexp.filename
        assertion_writer = AssertionWriter(use_regexp_assertion=True)
        assertion_writer.add_regular_expression('constant', '^[A-Z]+$')
        assertion_writer.write_assert_list(data, 'data', filename=filename)
        hash_digest = hash_file(filename)

        content = self.get_txt_content(filename)

        self.assertEqual(len(content), 16)
        self.assertEqual(content[0], 'self.assertEqual(len(data), 2)')
        self.assertEqual(content[1], 'self.assertEqual(data[0][\'config\'][\'bulding\'], 116)')
        self.assertEqual(content[2], 'self.assertEqual(data[0][\'config\'][\'server\'], \'all\')')
        self.assertEqual(content[3], 'self.assertEqual(len(data[0][\'groups\']), 2)')
        self.assertEqual(content[4], 'self.assertRegex(data[0][\'groups\'][0], r\'^[A-Z]+$\')')
        self.assertEqual(content[5], 'self.assertRegex(data[0][\'groups\'][1], r\'^[A-Z]+$\')')
        self.assertEqual(content[6], 'self.assertEqual(data[0][\'name\'], \'kilo\')')
        self.assertEqual(content[7], 'self.assertEqual(data[0][\'password\'], 9999)')
        self.assertEqual(content[8], 'self.assertEqual(data[1][\'config\'][\'bulding\'], 116)')
        self.assertEqual(content[9], 'self.assertEqual(data[1][\'config\'][\'server\'], \'database\')')
        self.assertEqual(content[10], 'self.assertRegex(data[1][\'cost\'], r\'^(\d+\.\d+)$\')')
        self.assertEqual(content[11], 'self.assertEqual(len(data[1][\'groups\']), 1)')
        self.assertEqual(content[12], 'self.assertEqual(data[1][\'groups\'][0], \'users\')')
        self.assertEqual(content[13], 'self.assertEqual(data[1][\'name\'], \'pasto\')')
        self.assertEqual(content[14], 'self.assertEqual(data[1][\'password\'], \'nogo\')')
        self.assertEqual(content[15], 'self.assertRegex(data[1][\'time\'], r\'^([0-1][0-9]|2[0-4]):([0-5][0-9])$\')')

    def test__build_assertion_datetime(self):
        date_time = datetime(2017, 2, 21, 14, 45, 4, tzinfo=pytz.UTC)
        assertion_list = list()
        self.writer._build_equals_assertion('date_time', date_time, assertion_list)
        expected_result = "self.assertEqual(date_time.strftime('%Y-%m-%d %H:%M:%S%z'), '2017-02-21 14:45:04+0000')"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])

    def test__build_assertion_datetime(self):
        date_time = datetime(2017, 2, 21, 14, 45, 4, tzinfo=pytz.UTC)
        assertion_list = list()
        self.writer._build_equals_assertion('date_time', date_time, assertion_list)
        expected_result = "self.assertEqual(date_time.strftime('%Y-%m-%d %H:%M:%S%z'), '2017-02-21 14:45:04+0000')"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])

    def test__build_assertion_date(self):
        date_value = date(2017, 2, 21)
        assertion_list = list()
        self.writer._build_equals_assertion('date_value', date_value, assertion_list)
        expected_result = "self.assertEqual(date_value.strftime('%Y-%m-%d'), '2017-02-21')"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])

    def test__build_assertion_decimal(self):
        decimal_value = Decimal(34.5)
        assertion_list = list()
        self.writer._build_equals_assertion('decimal_value', decimal_value, assertion_list)
        expected_result = "self.assertEqual(decimal_value, Decimal(34.5))"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])

    def test__build_assertion_string_with_quotes(self):
        string_var = r"The quoted values is 'KILO'"
        assertion_list = list()
        self.writer._build_equals_assertion('string_var', string_var, assertion_list)
        expected_result = "self.assertEqual(string_var, 'The quoted values is \\'KILO\\'')"
        self.assertEqual(assertion_list[0], expected_result)
        eval(assertion_list[0])

    def test__build_type_assertion_string_with_quotes(self):
        string_var = r"The quoted values is 'KILO'"
        assertion_list = list()
        self.writer._build_type_assertion('string_var', string_var, assertion_list)
        expected_result = "self.assertIsNotNone(string_var) # Example: The quoted values is 'KILO'"
        self.assertEqual(assertion_list[0], expected_result)
        eval(assertion_list[0])

    def test__build_type_assertion_datetime(self):
        date_time = datetime(2017, 2, 21, 14, 45, 4, tzinfo=pytz.UTC)
        assertion_list = list()
        self.writer._build_type_assertion('date_time', date_time, assertion_list)
        expected_result = "self.assertRegex(date_time.strftime('%Y-%m-%d %H:%M:%S%z')," \
                          " r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))\s\d{2}:\d{2}:\d{2}\+\d{4}') " \
                          "# Example: 2017-02-21 14:45:04+0000"
        self.assertEqual(assertion_list[0], expected_result, )
        eval(assertion_list[0])

    def test__build_type_assertion_date(self):
        date_value = date(2017, 2, 21)
        assertion_list = list()
        self.writer._build_type_assertion('date_value', date_value, assertion_list)
        expected_result = "self.assertRegex(date_value.strftime('%Y-%m-%d')," \
                          " r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))') # Example: 2017-02-21"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])

    def test__build_type_assertion_decimal(self):
        decimal_value = Decimal(34.5)
        assertion_list = list()
        self.writer._build_type_assertion('decimal_value', decimal_value, assertion_list)
        expected_result = "self.assertIsNotNone(decimal_value) # Example: Decimal(34.5)"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])
