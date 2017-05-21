PRINT_IMPORTS = """
from django.forms.models import model_to_dict
from django.conf import settings
from django.test import TestCase


"""
PRINT_FACTORY_CLASS= """
class TestCase{0}(TestCase):

    def test_create(self):
        \"\"\"
        Tesst the creation of a {0} model using a factory
        \"\"\"
        {1} = {0}Factory.create()
        self.assertEqual(1, {0}.objects.count())

    def test_create_batch(self):
        \"\"\"
        Tesst the creation of 5 {0} models using a factory
        \"\"\"
        {1}s = {0}Factory.create_batch(5)
        self.assertEqual(5, {0}.objects.count())
        self.assertEqual(5, len({1}s))
"""

PRINT_TEST_ATTRIBUTE_COUNT="""
    def test_attribute_count(self):
        \"\"\"
        Test that all attributes of {0} server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        \"\"\"
        {1} = {0}Factory.create()
        {1}_dict = model_to_dict({1})
        self.assertEqual({2}, len({1}_dict.keys()))
"""
PRINT_TEST_ATTRIBUTE_CONTENT="""
    def test_attribute_content(self):
        \"\"\"
        Test that all attributes of {0} server have content. This test will break if an attributes name is changed.
        \"\"\"
        {1} = {0}Factory.create()
"""

class ModelTestCaseGenerator(object):

    def __init__(self, model):
        self.model = model

    def _generate(self):
        factory_class_content = list()
        factory_class_content.append({'print': PRINT_FACTORY_CLASS,
                                      'args': [self.model.__name__, self.model.__name__.lower()]})
        factory_class_content.append({'print': PRINT_TEST_ATTRIBUTE_COUNT,
                                      'args': [self.model.__name__,
                                               self.model.__name__.lower(),
                                               len(self.model._meta.fields)]})

        content_text = PRINT_TEST_ATTRIBUTE_CONTENT.format(self.model.__name__,
                                                            self.model.__name__.lower())
        for field in self.model._meta.fields:
            field_type = type(field).__name__
            field_data = dict()
            assertion = '        self.assertNotNone({0}.{1})\n'.format(self.model.__name__.lower(), field.name)
            content_text +=  assertion

        factory_class_content.append({'print': content_text, 'args': None})




        return factory_class_content

    def __str__(self):
        printable = list()
        printable.append(PRINT_IMPORTS)
        for print_data in self._generate():
            try:
                if print_data['args'] is not None:
                    printable.append(print_data['print'].format(*print_data['args']))
                else:
                    printable.append(print_data['print'])
            except IndexError as e:
                print('-'*74)
                print('{print} {args}'.format(**print_data))
                raise e

        return '\n'.join(printable)


