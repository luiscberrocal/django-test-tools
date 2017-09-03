from django.core.management import BaseCommand

from ...app_manager import DjangoAppManager
from ...generators.model_test_gen import AppModelsTestCaseGenerator


class Command(BaseCommand):
    """

        $ python manage.py
    """

    def add_arguments(self, parser):
        parser.add_argument('app_name')
        # parser.add_argument("-l", "--list",
        #                     action='store_true',
        #                     dest="list",
        #                     help="List employees",
        #                     )
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
        app_manager = DjangoAppManager()
        app = app_manager.get_app(app_name)
        if app:
            app_model_tests = AppModelsTestCaseGenerator(app)
            self.stdout.write(str(app_model_tests))
