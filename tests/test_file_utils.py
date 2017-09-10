import os
import pickle
import shutil
from datetime import date, datetime
from unittest import mock

import pytz
from django.conf import settings
from django.test import TestCase, override_settings
from django.test import tag

from django_test_tools.file_utils import hash_file, temporary_file, serialize_data, add_date, create_dated
from django_test_tools.mixins import TestOutputMixin
from django_test_tools.utils import create_output_filename_with_date


class PersonObject(object):
    attributes = dict()

    def __init__(self, id, name, **kwargs):
        self.id = id,
        self.name = name
        self.attributes = kwargs

class AddDateTest(TestCase):
    def setUp(self):
        self.mock_datetime = pytz.timezone('America/Panama').localize(
            datetime.strptime('2016-07-07 16:40:39', '%Y-%m-%d %H:%M:%S'))

    @mock.patch('django.utils.timezone.now')
    def test_add_date_suffix_path(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date(filename)

        self.assertEquals(r'c:\kilo\poli\namos_20160707_1640.txt', new_filename)

        filename = r'c:\kilo\poli\namos.nemo.txt'
        new_filename = add_date(filename)

        self.assertEquals(r'c:\kilo\poli\namos.nemo_20160707_1640.txt', new_filename)

        filename = r'/my/linux/path/namos.nemo.txt'
        new_filename = add_date(filename)

        self.assertEquals(r'/my/linux/path/namos.nemo_20160707_1640.txt', new_filename)

    @mock.patch('os.path.exists')
    @mock.patch('django.utils.timezone.now')
    def test_add_date_suffix_path_existing_file(self, mock_now, mock_exists):
        mock_now.return_value = self.mock_datetime
        mock_exists.return_value = True

        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date(filename)

        self.assertEquals(r'c:\kilo\poli\namos_20160707_164039.txt', new_filename)

        filename = r'c:\kilo\poli\namos.nemo.txt'
        new_filename = add_date(filename)
        self.assertEquals(r'c:\kilo\poli\namos.nemo_20160707_164039.txt', new_filename)

        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date(filename, date_position='prefix')
        self.assertEquals(r'c:\kilo\poli\20160707_164039_namos.txt', new_filename)

        filename = r'/my/linux/path/namos.nemo.txt'
        new_filename = add_date(filename)

        self.assertEquals(r'/my/linux/path/namos.nemo_20160707_164039.txt', new_filename)

    @mock.patch('django.utils.timezone.now')
    def test_add_date_preffix_path(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'c:\kilo\poli\namos.txt'
        new_filename = add_date(filename, date_position='prefix')
        self.assertEquals(r'c:\kilo\poli\20160707_1640_namos.txt', new_filename)

        filename = r'/my/linux/path/namos.txt'
        new_filename = add_date(filename, date_position='prefix')
        self.assertEquals(r'/my/linux/path/20160707_1640_namos.txt', new_filename)

    @mock.patch('django.utils.timezone.now')
    def test_add_date_suffix_filename(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'namos.txt'
        new_filename = add_date(filename)
        self.assertEqual('namos_20160707_1640.txt', new_filename)

    @mock.patch('django.utils.timezone.now')
    def test_add_date_path(self, mock_now):
        mock_now.return_value = self.mock_datetime
        filename = r'/user/kilo/folder'
        new_filename = add_date(filename)
        self.assertEqual('/user/kilo/folder_20160707_1640', new_filename)


class CreateDatedTest(TestCase):
    @override_settings(TEST_OUTPUT_PATH=None)
    def test_create_output_filename_with_date_error(self):
        try:
            create_dated('kilo.txt')
            self.fail('Should have thrown value error')
        except ValueError as e:
            msg = 'You need a the variable TEST_OUTPUT_PATH in settings.' \
                  ' It should point to a folderfor temporary data to be written and reviewed.'
            self.assertEqual(msg, str(e))


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
            {'name': 'Luis', 'username': 'batman', 'date': date(2017, 7, 31), 'age': 25,
             'last_login': datetime(2016, 1, 1, 13, 14)},
            {'name': 'John', 'username': 'superman', 'date': date(2017, 8, 30), 'age': 45,
             'last_login': None, 'config': {'server': 'nostro', 'ip': 143443}},
            {'name': 'John', 'username': 'superman', 'date': date(2017, 8, 30), 'age': 45,
             'last_login': None, 'groups': ['admin', 'users']},
        ]
        filename = serialize_data(data)
        hash_digest = hash_file(filename)
        # self.clean_output=False
        self.clean_output_folder(filename)
        self.assertEqual('f1ef22b63e9708c37189c71c4d3ebc931d9ec220', hash_digest)
        self.assertFalse(os.path.exists(filename))

    @temporary_file('json')
    def test_serialize_dict_with_filename(self):
        data = [
            {'name': 'Luis', 'username': 'batman', 'date': date(2017, 7, 31), 'age': 25,
             'last_login': datetime(2016, 1, 1, 13, 14)},
            {'name': 'John', 'username': 'superman', 'date': date(2017, 8, 30), 'age': 45,
             'last_login': None, 'config': {'server': 'nostro', 'ip': 143443}},
            {'name': 'John', 'username': 'superman', 'date': date(2017, 8, 30), 'age': 45,
             'last_login': None, 'groups': ['admin', 'users']},
        ]
        filename = serialize_data(data, self.test_serialize_dict_with_filename.filename)
        hash_digest = hash_file(filename)
        self.assertEqual('f1ef22b63e9708c37189c71c4d3ebc931d9ec220', hash_digest)
        # self.assertFalse(os.path.exists(filename))

    def test_serialize_dict_with_folder(self):
        data = [
            {'name': 'Luis', 'username': 'batman', 'date': date(2017, 7, 31), 'age': 25,
             'last_login': datetime(2016, 1, 1, 13, 14)},
            {'name': 'John', 'username': 'superman', 'date': date(2017, 8, 30), 'age': 45,
             'last_login': None, 'config': {'server': 'nostro', 'ip': 143443}},
            {'name': 'John', 'username': 'superman', 'date': date(2017, 8, 30), 'age': 45,
             'last_login': None, 'groups': ['admin', 'users']},
        ]
        folder = os.path.join(settings.TEST_OUTPUT_PATH, 'test_serialize_dict_with_folder')
        if os.path.exists(folder):
            if os.path.isfile(folder):
                os.remove(folder)
                os.mkdir(folder)
            else:
                shutil.rmtree(folder)
                os.mkdir(folder)
        else:
            os.mkdir(folder)
        filename = serialize_data(data, folder)
        filename_path = os.path.split(filename)[0]
        hash_digest = hash_file(filename)
        self.assertEqual(folder, filename_path)
        self.assertEqual('f1ef22b63e9708c37189c71c4d3ebc931d9ec220', hash_digest)
        if self.clean_output:
            shutil.rmtree(folder)
        self.assertFalse(os.path.exists(filename))

    @temporary_file('json')
    def test_serialize_dict_invalid_format(self):
        data = [
            {'name': 'Luis', 'username': 'batman', 'date': date(2017, 7, 31), 'age': 25,
             'last_login': datetime(2016, 1, 1, 13, 14)},
            {'name': 'John', 'username': 'superman', 'date': date(2017, 8, 30), 'age': 45,
             'last_login': None, 'config': {'server': 'nostro', 'ip': 143443}},
            {'name': 'John', 'username': 'superman', 'date': date(2017, 8, 30), 'age': 45,
             'last_login': None, 'groups': ['admin', 'users']},
        ]
        try:
            serialize_data(data, self.test_serialize_dict_invalid_format.filename, format='POL')
            self.fail('Did not throw error for unsupported format')
        except AssertionError as e:
            self.assertEqual('Unsupported format POL', str(e))

    @temporary_file('pkl')
    def test_serialize_pickle(self):

        data = PersonObject(2, 'Batman', age=45, sex='M')

        serialize_data(data, self.test_serialize_pickle.filename, format='pickle')

        with open(self.test_serialize_pickle.filename, 'rb') as input:
            pickled_person = pickle.load(input)
        self.assertEqual(data.id, pickled_person.id)
        self.assertEqual(data.name, pickled_person.name)
        self.assertEqual(data.attributes['age'], pickled_person.attributes['age'])
        self.assertEqual(data.attributes['sex'], pickled_person.attributes['sex'])



