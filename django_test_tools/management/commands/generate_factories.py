from django.core.management import BaseCommand
from django.apps.registry import apps
PRINT_FACTORY_CLASS= """
class {0}Factory(DjangoModelFactory):
    class Meta:
        model = {0}
"""

PRINT_CHARFIELD ="""    {} = LazyAttribute(lambda x: FuzzyText(length=6, chars=string.digits).fuzz()){}"""
PRINT_DATETIMEFIELD ="""    {} = LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", end_date="-1d")){}"""
PRINT_FOREIGNKEY ="""    {} = SubFactory({}Factory){}"""

class Command(BaseCommand):
    """

        $ python manage.py
    """

    def add_arguments(self, parser):
        pass
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
        app = options.get('app_name')
        installed_apps = dict(self.get_apps())
        app = installed_apps.get(app)
        for model in app.get_models():
            self.stdout.write(PRINT_FACTORY_CLASS.format(model.__name__))
            for field in model._meta.fields:
                if type(field).__name__ in  ['AutoField', 'AutoCreatedField', 'AutoLastModifiedField']:
                    pass
                elif type(field).__name__ == 'DateTimeField':
                    self.stdout.write(PRINT_DATETIMEFIELD.format(field.name,''))
                elif type(field).__name__ == 'CharField':
                    self.stdout.write(PRINT_CHARFIELD.format(field.name,''))
                elif type(field).__name__ == 'ForeignKey':
                    related_model = field.rel.to.__name__
                    self.stdout.write(PRINT_FOREIGNKEY.format(field.name, related_model,''))
                else:
                    self.stdout.write(PRINT_CHARFIELD.format(field.name, '#' +type(field).__name__))

            self.stdout.write('-'*25)




    def get_apps(self):
        for app_config in apps.get_app_configs():
            yield app_config.name, app_config
