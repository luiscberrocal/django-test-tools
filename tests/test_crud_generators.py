import os
from django.test import TestCase

from django_test_tools.file_utils import hash_file, temporary_file
from django_test_tools.generators.crud_generator import UrlGenerator


class TestUrlGenerator(TestCase):

    @temporary_file('.py', delete_on_exit=True)
    def test_print_urls(self):
        filename = self.test_print_urls.filename
        generator = UrlGenerator('Server')
        generator.print_urls(filename)
        self.assertTrue(os.path.exists(filename))
        hash = hash_file(filename)
        self.assertEqual(hash, '14ef340ea846e3d37fd71d80362a5225e05133a3')

    @temporary_file('.py', delete_on_exit=True)
    def test_print_paths(self):
        filename = self.test_print_paths.filename
        generator = UrlGenerator('Server')
        generator.print_paths(filename)
        self.assertTrue(os.path.exists(filename))
        hash = hash_file(filename)
        self.assertEqual(hash, 'de4251b6c78a5911b6c3440c580de05d4d417c59')
