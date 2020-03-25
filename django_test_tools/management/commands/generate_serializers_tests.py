import importlib

from django.core.management import BaseCommand

from ...generators.crud_generator import SerializerTestGenerator


class Command(BaseCommand):
    """

        $ python manage.py generate_serializers_test my_application.app.api.serializers.MyObjectSerializer -f output/m.py
    """

    def add_arguments(self, parser):
        parser.add_argument('serializer_class')

        parser.add_argument("-f", "--filename",
                            dest="filename",
                            help="Output filename",
                            )

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
