from django.core.management import call_command
from django.test import TestCase

from django_test_tools.mixins import TestCommandMixin


class TestGenerateFactories(TestCommandMixin, TestCase):

    def test_generate(self):
        call_command('generate_factories', 'example.my_app', stdout=self.content)
        results = self.get_results()
        self.assertEqual(41, len(results))
