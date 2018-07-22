from django.core.management import BaseCommand

from ...app_manager import DjangoAppManager

PRINT_IMPORTS = """
import string

from random import randint
from pytz import timezone

from django.conf import settings

from factory import Iterator
from factory import LazyAttribute
from factory import SubFactory
from factory import lazy_attribute
from factory.django import DjangoModelFactory, FileField
from factory.fuzzy import FuzzyText, FuzzyInteger
from faker import Factory as FakerFactory

faker = FakerFactory.create()

"""
PRINT_FACTORY_CLASS = """
class {0}Factory(DjangoModelFactory):
    class Meta:
        model = {0}
"""

PRINT_CHARFIELD = """    {} = LazyAttribute(lambda x: faker.text(max_nb_chars={}))"""
PRINT_CHARFIELD_NUM = """    {} = LazyAttribute(lambda x: FuzzyText(length={}, chars=string.digits).fuzz())"""
PRINT_CHARFIELD_LETTERS = """    {} = LazyAttribute(lambda x: FuzzyText(length={}, chars=string.ascii_letters).fuzz())"""
PRINT_CHARFIELD_CHOICES = """    {} = Iterator({}.{}, getter=lambda x: x[0])"""
PRINT_DATETIMEFIELD = """    {} = LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", end_date="now",
                                                           tzinfo=timezone(settings.TIME_ZONE)))"""
PRINT_FOREIGNKEY = """    {} = SubFactory({}Factory){}"""
PRINT_FILEFIELD = """    {} = FileField(filename='{}.{}')"""
PRINT_BOOLEANFIELD = """    {} = Iterator([True, False])"""
PRINT_INTEGERFIELD = """    {} = LazyAttribute(lambda o: randint(1, 100))"""
PRINT_IPADDRESSFIELD = """    {} = LazyAttribute(lambda o: faker.ipv4(network=False))"""
PRINT_TEXTFIELD = """    {} = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))"""
PRINT_DECIMALFIELD = """    {} = LazyAttribute(lambda x: faker.pydecimal(left_digits={}, right_digits={}, positive=True))"""
PRINT_UNSUPPORTED_FIELD = """    #{} = {} We do not support this field type"""
PRINT_COUNTRYFIELD = """    {} = Iterator(['PA', 'US'])"""


# noinspection PyProtectedMember
class ModelFactoryGenerator(object):
    def __init__(self, model):
        self.model = model

    def _generate(self):
        factory_class_content = list()
        factory_class_content.append({'print': PRINT_FACTORY_CLASS, 'args': [self.model.__name__]})
        for field in self.model._meta.fields:
            field_type = type(field).__name__
            field_data = dict()
            if field_type in ['AutoField', 'AutoCreatedField', 'AutoLastModifiedField']:
                pass
            elif field_type in ['DateTimeField', 'DateField']:
                field_data = {'print': PRINT_DATETIMEFIELD, 'args': [field.name]}
                factory_class_content.append(field_data)
            elif field_type == 'CharField':
                field_data = self._get_charfield(field)
                factory_class_content.append(field_data)
            elif field_type == 'ForeignKey':
                related_model = field.remote_field.model.__name__
                field_data = {'print': PRINT_FOREIGNKEY,
                              'args': [field.name, related_model, '']}
                factory_class_content.append(field_data)
            elif field_type == 'BooleanField':
                field_data = {'print': PRINT_BOOLEANFIELD, 'args': [field.name]}
                factory_class_content.append(field_data)

            elif field_type == 'TextField':
                field_data = {'print': PRINT_TEXTFIELD, 'args': [field.name]}
                factory_class_content.append(field_data)

            elif field_type == 'IntegerField':
                field_data = {'print': PRINT_INTEGERFIELD, 'args': [field.name]}
                factory_class_content.append(field_data)

            elif field_type == 'FileField':
                field_data = {'print': PRINT_FILEFIELD, 'args': [field.name, field.name, 'xlsx']}
                factory_class_content.append(field_data)

            elif field_type == 'DecimalField' or field_type == 'MoneyField':
                max_left = field.max_digits - field.decimal_places
                max_right = field.decimal_places
                field_data = {'print': PRINT_DECIMALFIELD,
                              'args': [field.name, max_left, max_right]}
                factory_class_content.append(field_data)

            elif field_type == 'GenericIPAddressField':
                field_data = {'print': PRINT_IPADDRESSFIELD, 'args': [field.name]}
                factory_class_content.append(field_data)

            elif field_type == 'CountryField':
                field_data = {'print': PRINT_COUNTRYFIELD, 'args': [field.name]}
                factory_class_content.append(field_data)
            else:
                field_data = {'print': PRINT_UNSUPPORTED_FIELD,
                              'args': [field.name, field_type]}
                factory_class_content.append(field_data)

        return factory_class_content

    def _get_charfield(self, field):
        field_data = dict()
        if len(field.choices) > 0:
            field_data = {'print': PRINT_CHARFIELD_CHOICES, 'args': [field.name, self.model.__name__, 'CHOICES']}
            return field_data
        else:
            if self._is_number(field.name):
                field_data = {'print': PRINT_CHARFIELD_NUM,
                              'args': [field.name, field.max_length]}
                return field_data
            else:
                if field.max_length >= 5:
                    field_data = {'print': PRINT_CHARFIELD,
                                  'args': [field.name, field.max_length]}
                else:
                    field_data = {'print': PRINT_CHARFIELD_LETTERS,
                                  'args': [field.name, field.max_length]}
                return field_data

    def _is_number(self, field_name):
        num_vals = ['id', 'num']
        for nv in num_vals:
            if nv in field_name.lower():
                return True
        return False

    def __str__(self):
        printable = list()
        for print_data in self._generate():
            try:
                printable.append(print_data['print'].format(*print_data['args']))
            except IndexError as e:
                print('-' * 74)
                print('{print} {args}'.format(**print_data))
                raise e

        return '\n'.join(printable)


class Command(BaseCommand):
    """

        $ python manage.py generate_factories project.app
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
        app_name = options.get('app_name')
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
