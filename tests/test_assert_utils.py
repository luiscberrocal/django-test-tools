from datetime import datetime, date

import pytz
from decimal import Decimal
from django.test import TestCase

from django_test_tools.assert_utils import write_assert_list, AssertionWriter
import logging

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
        self.assertEqual('self.assertEqual(1, len(data))', results[0])

    @temporary_file('py', delete_on_exit=True)
    def test_write_assert_list(self):
        data = [
            {'name': 'kilo', 'password': 9999,
             'groups': ['admin', 'users'],
             'config':{'server': 'all', 'bulding': 116}},
            {'name': 'pasto', 'password': 'nogo',
             'groups': ['users'],
             'config': {'server': 'database', 'bulding': 116}}
        ]
        filename = write_assert_list(self.test_write_assert_list.filename, data, 'data')
        self.assertEqual(filename, self.test_write_assert_list.filename)
        hash_digest = hash_file(filename)
        self.assertEqual('2848cab5285d55c71f727aee4e966914f51dd4ee', hash_digest)

    def test_build_assertion_datetime(self):
        date_time = datetime(2017, 2, 21, 14, 45, 4, tzinfo=pytz.UTC)
        assertion_list = list()
        self.writer._build_assertion('date_time', date_time, assertion_list)
        expected_result = "self.assertEqual('2017-02-21 14:45:04+0000', date_time.strftime('%Y-%m-%d %H:%M:%S%z'))"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])

    def test_build_assertion_date(self):
        date_value = date(2017, 2, 21)
        assertion_list = list()
        self.writer._build_assertion('date_value', date_value, assertion_list)
        expected_result = "self.assertEqual('2017-02-21', date_value.strftime('%Y-%m-%d'))"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])

    def test_build_assertion_decimal(self):
        decimal_value = Decimal(34.5)
        assertion_list = list()
        self.writer._build_assertion('decimal_value', decimal_value, assertion_list)
        expected_result = "self.assertEqual(Decimal(34.5), decimal_value)"
        self.assertEqual(expected_result, assertion_list[0])
        eval(assertion_list[0])

