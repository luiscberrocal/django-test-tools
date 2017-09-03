import logging
import os
import shutil

from django.conf import settings
from django.test import TestCase

from django_test_tools.doc_utils.folder_structure import create_folder_structure, get_module_files
from django_test_tools.file_utils import serialize_data, temporary_file
from django_test_tools.utils import create_output_filename_with_date

logger = logging.getLogger(__name__)


class TestFolderStructure(TestCase):
    def test_create_folder_structure(self):
        # logger.debug('Version {}'.format(django.VERSION))
        folder = create_output_filename_with_date('docs')
        if not os.path.exists(folder):
            os.makedirs(folder)
        create_folder_structure(folder, 'django')
        django_apps = ['admin', 'auth', 'contenttypes', 'messages', 'sessions', 'staticfiles']
        for djanoo_app in django_apps:
            django_folder = os.path.join(folder, 'django', djanoo_app)
            self.assertTrue(os.path.exists(django_folder))
            index_file = os.path.join(django_folder, 'index.rst')
            self.assertTrue(os.path.exists(index_file))
            model_file = os.path.join(django_folder, 'django.contrib.{}.models.rst'.format(djanoo_app))
            self.assertTrue(os.path.exists(model_file))
        shutil.rmtree(folder)

    @temporary_file('json')
    def test_get_module_files(self):
        folder = str(settings.ROOT_DIR.path('example', 'servers'))
        # folder = str(settings.ROOT_DIR.path('django_test_tools'))
        files = get_module_files(folder)
        serialize_data(files, self.test_get_module_files.filename)
        # for file in files:
        #     logger.debug('File: {filename} Package: {package_name}'.format(**file))
        self.assertEqual(1, len(files))

    def test_create_folder_structure2(self):
        # logger.debug('Version {}'.format(django.VERSION))
        folder = create_output_filename_with_date('docs')
        if not os.path.exists(folder):
            os.makedirs(folder)
        create_folder_structure(folder, 'django_test_tools')
        shutil.rmtree(folder)
