from django.core.management import BaseCommand
from django.apps.registry import apps


PRINT_IMPORTS = """
import string

from pytz import timezone

from factory import Iterator
from factory import LazyAttribute
from factory import SubFactory
from factory import lazy_attribute
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyInteger
from faker import Factory as FakerFactory

faker = FakerFactory.create()

"""
PRINT_FACTORY_CLASS= """
class {0}Factory(DjangoModelFactory):
    class Meta:
        model = {0}
"""

PRINT_CHARFIELD ="""    {} = LazyAttribute(lambda x: faker.text(max_nb_chars={}))"""
PRINT_CHARFIELD_NUM ="""    {} = LazyAttribute(lambda x: FuzzyText(length={}, chars=string.digits).fuzz())"""
PRINT_CHARFIELD_CHOICES ="""    {} = Iterator({}.{}, getter=lambda x: x[0])"""
PRINT_DATETIMEFIELD ="""    {} = LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", end_date="now",
                                                           tzinfo=timezone(settings.TIME_ZONE))){}"""
PRINT_FOREIGNKEY ="""    {} = SubFactory({}Factory){}"""
PRINT_BOOLEANFIELD ="""    {} = Iterator([True, False])"""
PRINT_INTEGERFIELD ="""    {} = LazyAttribute(lambda o: randint(1, 100))"""
PRINT_IPADDRESSFIELD ="""    {} = LazyAttribute(lambda o: faker.ipv4(network=False))"""
PRINT_TEXTFIELD ="""    {} = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))"""
PRINT_DECIMAL ="""    {} = LazyAttribute(lambda x: faker.pydecimal(left_digits={}, right_digits={}, positive=True))"""



class ModelFactoryGenerator(object):

    def __init__(self, model):
        self.model = model

    def _generate(self):
        factory_class_content = list()
        factory_class_content.append(PRINT_FACTORY_CLASS.format(self.model.__name__))
        for field in self.model._meta.fields:
            field_type = type(field).__name__
            if field_type in ['AutoField', 'AutoCreatedField', 'AutoLastModifiedField']:
                pass
            elif field_type in ['DateTimeField', 'DateField']:
                factory_class_content.append(PRINT_DATETIMEFIELD.format(field.name, ''))
            elif field_type == 'CharField':
                factory_class_content.append(self._get_charfield(field))
            elif field_type == 'ForeignKey':
                related_model = field.rel.to.__name__
                factory_class_content.append(PRINT_FOREIGNKEY.format(field.name, related_model, ''))
            elif field_type == 'BooleanField':
                factory_class_content.append(PRINT_BOOLEANFIELD.format(field.name))
            elif field_type == 'TextField':
                factory_class_content.append(PRINT_TEXTFIELD.format(field.name))
            elif field_type == 'IntegerField':
                factory_class_content.append(PRINT_INTEGERFIELD.format(field.name))
            elif field_type == 'DecimalField':
                max_left = field.max_digits - field.decimal_places -1
                max_right = field.decimal_places
                factory_class_content.append(PRINT_DECIMAL.format(field.name, max_left, max_right))
            elif field_type == 'GenericIPAddressField':
                factory_class_content.append(PRINT_IPADDRESSFIELD.format(field.name))

            else:
                factory_class_content.append('     //{} = {} ******'.format(field.name, field_type))

        return factory_class_content

    def _get_charfield(self, field):
        if len(field.choices) > 0:
           return PRINT_CHARFIELD_CHOICES.format(field.name, self.model.__name__, 'CHOICES')
        else:
            if self._is_number(field.name):
                return PRINT_CHARFIELD_NUM.format(field.name, field.max_length)
            else:
                return PRINT_CHARFIELD.format(field.name, field.max_length, '')

    def _is_number(self, field_name):
        num_vals = ['id', 'num']
        for nv in num_vals:
            if nv in field_name.lower():
                return True
        return False

    def __str__(self):
        return '\n'.join(self._generate())


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
        self.stdout.write(PRINT_IMPORTS)
        for model in app.get_models():
            model_fact = ModelFactoryGenerator(model)
            self.stdout.write(str(model_fact))




    def get_apps(self):
        for app_config in apps.get_app_configs():
            yield app_config.name, app_config
