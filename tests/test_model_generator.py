from django.conf import settings
from django.test import TestCase

from django_test_tools.generators.model_generator import FactoryBoyGenerator


class TestFactoryBoyGenerator(TestCase):

    def test_(self):
        generator = FactoryBoyGenerator()
        data = generator.create_template_data(settings.TEST_APP)
#        self.assertEqual(data, '')
