import os

from django.test import TestCase

from django_test_tools.file_utils import create_dated, hash_file, temporary_file
from django_test_tools.generators.crud_generator import UrlGenerator


class TestUrlGenerator(TestCase):

    @temporary_file(',py', delete_on_exit=False)
    def test_print_urls(self):
        filename = self.test_print_urls.filename
        generator = UrlGenerator('Server')
        generator.print_urls(filename)
        self.assertTrue(os.path.exists(filename))
        hash = hash_file(filename)
        self.assertEqual(hash, '14ef340ea846e3d37fd71d80362a5225e05133a3')

