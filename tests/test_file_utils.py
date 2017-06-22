import os

from datetime import date, datetime
from django.conf import settings
from django.test import TestCase
from django.test import tag

from django_test_tools.file_utils import hash_file, temporary_file, serialize_dict
from django_test_tools.mixins import TestOutputMixin
from django_test_tools.utils import create_output_filename_with_date





@tag('UNIT')
class TestHashFile(TestOutputMixin, TestCase):

    def test_hash(self):
        filename = create_output_filename_with_date('test_hash.txt')
        my_list = ['1', 'hola', 'poli', 'kilo']
        with open(filename, 'w', encoding='utf-8') as mfile:
            mfile.writelines(my_list)
        hash = hash_file(filename)
        self.assertEqual('f753b70e9ef151b4b50ef33a0aa29ef2501c580e', hash)
        self.clean_output_folder(filename)

    def test_hash_invalid_algorithm(self):
        filename = create_output_filename_with_date('test_hash.txt')
        try:
            hash = hash_file(filename, algorithm='kkkk')
            self.fail('Should have sent exception')
        except ValueError as e:
            self.assertEqual('kkkk is not a valid hashing algorithm', str(e))

    @temporary_file('json')
    def test_temporary_file_decorator(self):
        head, tails = os.path.split(self.test_temporary_file_decorator.filename)
        self.assertEqual(settings.TEST_OUTPUT_PATH, head)
        self.assertRegexpMatches(tails, r'^test_temporary_file_decorator_\d{8}_\d{4}\.json')

        my_list = ['1', 'hola', 'poli', 'kilo']
        with open(self.test_temporary_file_decorator.filename, 'w', encoding='utf-8') as mfile:
            mfile.writelines(my_list)
        self.assertTrue(os.path.exists(self.test_temporary_file_decorator.filename))

    def test_temporary_file_decorator_no_delete(self):
        @temporary_file('xlsx', delete_on_exit=False)
        def my_function2():
            my_list = ['1', 'hola', 'poli', 'kilo']
            with open(my_function2.filename, 'w', encoding='utf-8') as mfile:
                mfile.writelines(my_list)
            return my_function2.filename

        filename = my_function2()
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

    def test_serialize_dict(self):
        data = [
            {'name': 'Luis', 'username': 'batman', 'date': date(2017,7,31), 'age': 25,
             'last_login': datetime(2016,1,1,13,14)},
            {'name': 'John', 'username': 'superman', 'date': date(2017,8,30), 'age': 45,
             'last_login': None, 'config': {'server': 'nostro', 'ip':143443}},
            {'name': 'John', 'username': 'superman', 'date': date(2017, 8, 30), 'age': 45,
             'last_login': None, 'groups': ['admin', 'users']},
        ]
        filename = serialize_dict(data)
        hash_digest = hash_file(filename)
        #self.clean_output=False
        self.clean_output_folder(filename)
        self.assertEqual('f1ef22b63e9708c37189c71c4d3ebc931d9ec220', hash_digest)

    def test_serialize_dict_invalid_format(self):
        data = [
            {'name': 'Luis', 'username': 'batman', 'date': date(2017,7,31), 'age': 25,
             'last_login': datetime(2016,1,1,13,14)},
            {'name': 'John', 'username': 'superman', 'date': date(2017,8,30), 'age': 45,
             'last_login': None, 'config': {'server': 'nostro', 'ip':143443}},
            {'name': 'John', 'username': 'superman', 'date': date(2017, 8, 30), 'age': 45,
             'last_login': None, 'groups': ['admin', 'users']},
        ]
        try:
            serialize_dict(data, format='POL')
        except AssertionError as e:
            self.assertEqual('Unsupported format POL', str(e))
