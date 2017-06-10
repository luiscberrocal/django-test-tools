import os

import shutil
from django.test import TestCase

from django_test_tools.doc_utils.folder_structure import create_folder_structure
from django_test_tools.utils import create_output_filename_with_date


class TestFolderStructure(TestCase):

    def test_create_folder_structure(self):
        folder = create_output_filename_with_date('docs')
        if not os.path.exists(folder):
            os.makedirs(folder)
        create_folder_structure(folder, 'django')
        django_apps = ['admin', 'auth', 'contenttypes']
        for djanoo_app in django_apps:
            django_folder = os.path.join(folder, 'django', djanoo_app)
            self.assertTrue(os.path.exists(django_folder))
        shutil.rmtree(folder)


