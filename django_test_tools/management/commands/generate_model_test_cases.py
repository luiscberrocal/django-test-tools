from django.core.management import BaseCommand

from ...app_manager import DjangoAppManager
from ...generators.model_test_gen import AppModelsTestCaseGenerator


class Command(BaseCommand):
    """
        $ python manage.py
    """

    def add_arguments(self, parser):
        parser.add_argument('app_name')

    def handle(self, *args, **options):
        app_name = options.get('app_name', None)
        app_manager = DjangoAppManager()
        app = app_manager.get_app(app_name)
        if app:
            app_model_tests = AppModelsTestCaseGenerator(app)
            self.stdout.write(str(app_model_tests))
