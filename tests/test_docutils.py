import os

from django.test import TestCase

from django_test_tools.doc_utils.folder_structure import create_folder_structure
from django_test_tools.utils import create_output_filename_with_date


class TestFolderStructure(TestCase):

    def test_(self):
        folder = create_output_filename_with_date('docs')
        if not os.path.exists(folder):
            os.makedirs(folder)
        p = create_folder_structure(folder, 'example')

