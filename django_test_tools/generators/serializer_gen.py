import logging

logger = logging.getLogger(__name__)
PRINT_IMPORTS = ['from rest_framework import serializers',]
PRINT_SERIALIZER_CLASS = """
class {0}Serializers(serializers.{1}):
    \"\"\"
    Standard Serializer for {0} model.
    \"\"\"

    class Meta:
        model = {0}
        fields = ({2})
"""

class SerializerGenerator(object):
    def __init__(self, model, serializer_class='ModelSerializer'):
        self.model = model
        self.serializer_class = serializer_class

    def _generate(self):
        model_test_case_content = list()

        field_names = list()
        for field in self.model._meta.fields:
            field_names.append('\'{}\''.format(field.name))

        model_test_case_content.append({'print': PRINT_SERIALIZER_CLASS,
                                        'args': [self.model.__name__,
                                                 self.serializer_class,
                                                 ', '.join(field_names)]})
        return model_test_case_content

    def __str__(self):
        printable = list()
        for print_data in self._generate():
            try:
                if print_data['args'] is not None:
                    printable.append(print_data['print'].format(*print_data['args']))
                else:
                    printable.append(print_data['print'])
            except IndexError as e:
                print('-' * 74)
                print('{print} {args}'.format(**print_data))
                raise e

        return '\n'.join(printable)


class AppSerializerGenerator(object):
    def __init__(self, app, serializer_class='ModelSerializer'):
        self.app = app
        self.serializer_class =serializer_class

    def _generate(self):
        app_content = list()
        for model in self.app.get_models():
            PRINT_IMPORTS.append('from {} import {}'.format(model.__module__, model.__name__))
            logger.debug('IMPORTS: {}'.format(PRINT_IMPORTS))
            model_test_case = SerializerGenerator(model, self.serializer_class)
            app_content.append(model_test_case)
        return app_content

    def _get_imports(self):
        logger.debug('IMPORTS: {}'.format(PRINT_IMPORTS))
        imports_to_print = list(set(PRINT_IMPORTS))
        imports_to_print.sort(reverse=True)
        return '\n'.join(imports_to_print)

    def __str__(self):
        printable = list()
        serializers_codes = self._generate()
        printable.append(self._get_imports())
        for serializers_code in serializers_codes:
            printable.append(str(serializers_code))

        return '\n'.join(printable)
