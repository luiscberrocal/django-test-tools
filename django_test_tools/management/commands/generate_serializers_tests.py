import importlib
import os

from django.core.management import BaseCommand

from django_test_tools.generators.crud_generator import SerializerTestGenerator
from ...file_utils import add_date
from ...flake8.parsers import Flake8Parser, RadonParser


class Command(BaseCommand):
    """

        $ python manage.py generate_serializers_test my_application.app.api.serializers.MyObjectSerializer -f output/m.py
    """

    def add_arguments(self, parser):
        parser.add_argument('serializer_class')
        # parser.add_argument("-l", "--list",
        #                     action='store_true',
        #                     dest="list",
        #                     help="List employees",
        #                     )
        parser.add_argument("-f", "--filename",
                            dest="filename",
                            help="Output filename",
                            )
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
        parts = options.get('serializer_class').split('.')
        serializer_class_name = parts[-1]
        module_name = '.'.join(parts[0:-1])
        filename = options.get('filename')
        generator = SerializerTestGenerator()
        data = dict()
        my_module = importlib.import_module(module_name)
        MySerializer = getattr(my_module, serializer_class_name)

        serializer = MySerializer()
        rep_ser = repr(serializer)
        fields = list()
        str_fields = list()
        for field in serializer.fields:
            fields.append(field)

        for key, field in serializer.fields.fields.items():
            if type(field).__name__ in ['CharField', 'TextField']:
                str_fields.append(field.field_name)
            print(key)

        data['model_name'] = serializer.Meta.model.__name__
        data['fields'] = fields
        data['string_vars'] = str_fields
        generator.print(data, filename)
        self.stdout.write('Printed to file {}'.format(filename))
