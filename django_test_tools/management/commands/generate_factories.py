import os

from django.conf import settings
from django.core.management import BaseCommand

from django_test_tools.generators.crud_generator import GenericTemplateWriter
from django_test_tools.generators.model_generator import FactoryBoyGenerator
from ..._legacy.management.commands.generate_factories import PRINT_IMPORTS, ModelFactoryGenerator
from ...app_manager import DjangoAppManager


# noinspection PyProtectedMember


class Command(BaseCommand):
    """
        $ python manage.py generate_factories project.app --filename=_factories.py
    """

    def add_arguments(self, parser):
        parser.add_argument('app_name')
        parser.add_argument("-f", "--filename",
                            dest="filename",
                            help="Output filename",
                            default=None,
                            )

    def handle(self, *args, **options):
        app_name = options.get('app_name')
        if options.get('filename'):
            filename = os.path.join(settings.TEST_OUTPUT_PATH, options.get('filename'))
            generator = FactoryBoyGenerator()
            factory_data = generator.create_template_data(app_name)
            template_name = 'factories.py.j2'
            writer = GenericTemplateWriter(template_name)
            writer.write(factory_data, filename)
        else:
            app_manager = DjangoAppManager()
            app = app_manager.get_app(app_name)
            if not app:
                self.stderr.write('This command requires an existing app name as '
                                  'argument')
                self.stderr.write('Available apps:')
                for app in sorted(app_manager.installed_apps):
                    self.stderr.write('    %s' % app)
            else:
                self.stdout.write(PRINT_IMPORTS)
                for model in app.get_models():
                    model_fact = ModelFactoryGenerator(model)
                    self.stdout.write(str(model_fact))
