from django.test import TestCase

from django_test_tools.file_utils import hash_file
from django_test_tools.mixins import TestOutputMixin
from django_test_tools.utils import create_output_filename_with_date


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

