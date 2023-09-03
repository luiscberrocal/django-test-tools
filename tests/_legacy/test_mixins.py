from django.test import SimpleTestCase

from django_test_tools._legacy.mixins import TestFixtureMixin


class TestTestFixtureMixin(SimpleTestCase):
    """
    The fixtures for this test are located at django-test-tools/django_test_tools/tests/fixtures because I could not
    figure how to read the fixtures from the django-test-tools/tests/fixtures folders. TODO Figure how to fix that
    """

    def test_get_fixture_json(self):
        mixin = TestFixtureMixin(app_name=None, strict=False)
        celery_data = mixin.get_fixture_json('celery.json')
        self.assertEqual(len(celery_data), 2)

    def test_get_fixture_fullpath(self):
        mixin = TestFixtureMixin(app_name=None, strict=False)
        filename = mixin.get_fixture_fullpath('base.txt')
        self.assertTrue('/django_test_tools/tests/fixtures/base.txt' in filename)
