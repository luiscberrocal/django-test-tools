from django.apps import apps
from django.core.management import BaseCommand

from django_test_tools.generators.serializer_gen import AppSerializerGenerator
from ...app_manager import DjangoAppManager
from ...generators.model_test_gen import AppModelsTestCaseGenerator


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
        serializer_class = options.get('serializer_class')
        app_manager = DjangoAppManager()
        app = app_manager.get_app(app_name)
        if app:
            app_model_tests = AppSerializerGenerator(app, serializer_class)
            self.stdout.write(str(app_model_tests))
