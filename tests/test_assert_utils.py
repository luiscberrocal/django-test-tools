import logging
from datetime import datetime, date
from decimal import Decimal

import pytz
from django.test import TestCase

from django_test_tools.assert_utils import write_assert_list, AssertionWriter
from django_test_tools.file_utils import temporary_file, hash_file

logger = logging.getLogger(__name__)


class TestAssertionWriter(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.writer = AssertionWriter()

    def test_generate_assert_equals_dictionaries(self):
        data = [
            {'name': 'kilo', 'password': 9999, 'groups': ['admin', 'users']}
        ]

        results = self.writer._generate_assert_equals_list(data, 'data')
        self.assertEqual(results[0], 'self.assertEqual(len(data), 1)')

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

    def test__build_assertion_datetime(self):
        date_time = datetime(2017, 2, 21, 14, 45, 4, tzinfo=pytz.UTC)
        assertion_list = list()
        self.writer._build_assertion('date_time', date_time, assertion_list)
        expected_result = "self.assertEqual(date_time.strftime('%Y-%m-%d %H:%M:%S%z'), '2017-02-21 14:45:04+0000')"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])

    def test__build_assertion_date(self):
        date_value = date(2017, 2, 21)
        assertion_list = list()
        self.writer._build_assertion('date_value', date_value, assertion_list)
        expected_result = "self.assertEqual(date_value.strftime('%Y-%m-%d'), '2017-02-21')"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])

    def test__build_assertion_decimal(self):
        decimal_value = Decimal(34.5)
        assertion_list = list()
        self.writer._build_assertion('decimal_value', decimal_value, assertion_list)
        expected_result = "self.assertEqual(decimal_value, Decimal(34.5))"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])

    def test__build_assertion_string_with_quotes(self):
        string_var = r"The quoted values is 'KILO'"
        assertion_list = list()
        self.writer._build_assertion('string_var', string_var, assertion_list)
        expected_result = "self.assertEqual(string_var, 'The quoted values is \\'KILO\\'')"
        self.assertEqual(assertion_list[0], expected_result)
        eval(assertion_list[0])
