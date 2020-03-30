import os

from django.conf import settings
from django.core.management import BaseCommand

from django_test_tools.generators.crud_generator import GenericTemplateWriter
from django_test_tools.generators.model_generator import ModelSerializerGenerator
from ...generators.serializer_gen import AppSerializerGenerator
from ...app_manager import DjangoAppManager


class Command(BaseCommand):
    """

        $ python manage.py generate_serializers project.app -s ModelSerializer
    """

    def add_arguments(self, parser):
        parser.add_argument('app_name')
        parser.add_argument("-s", "--serializer-class",
                            dest="serializer_class",
                            help="Serializer class",
                            default='ModelSerializer'
                            )
        parser.add_argument('-f', "--filename",
                            dest="filename",
                            help="Output filename. Will write it to the settings.TEST_OUTPUT_PATH folder",
                            default=None,
                            )
        # parser.add_argument("-a", "--assign",
        #                     action='store_true',
        #                     dest="assign",
        #                     help="Create unit assignments",
        #                     )
        #
        # parser.add_argument("--office",
        #                     dest="office",
        #                     help="Organizational unit short name",
        #                     default=None,
        #                     )
        # parser.add_argument("--start-date",
        #                     dest="start_date",
        #                     help="Start date for the assignment",
        #                     default=None,
        #                     )
        # parser.add_argument("--fiscal-year",
        #                     dest="fiscal_year",
        #                     help="Fiscal year for assignments",
        #                     default=None,
        #                     )
        # parser.add_argument("-u", "--username",
        #                 dest="usernames",
        #                 help="LDAP usernames for employees",
        #                 nargs='+',
        #                 )

    def handle(self, *args, **options):
        app_name = options.get('app_name', None)
        if options.get('filename'):
            filename = os.path.join(settings.TEST_OUTPUT_PATH, options.get('filename'))
            generator = ModelSerializerGenerator()
            factory_data = generator.create_template_data(app_name)
            template_name = 'serializers.py.j22'
            writer = GenericTemplateWriter(template_name)
            writer.write(factory_data, filename)
        else:
            serializer_class = options.get('serializer_class')
            app_manager = DjangoAppManager()
            app = app_manager.get_app(app_name)
            if app:
                app_model_tests = AppSerializerGenerator(app, serializer_class)
                self.stdout.write(str(app_model_tests))
