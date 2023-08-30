import json
from pathlib import Path

from django.test import SimpleTestCase

from django_test_tools.generators.models import FieldInfo


class TestModels(SimpleTestCase):

    def test_deserializing_file(self):
        file = Path(__file__).parent.parent / 'fixtures' / 'servers_models.json'
        self.assertTrue(file.exists())
        with open(file, 'r') as f:
            server_dict = json.load(f)
        for model_name in server_dict['models'].keys():
            for field_dict in server_dict['models'][model_name]['fields']:
                try:
                    field_info = FieldInfo(**field_dict)
                    self.assertEqual(field_info.field_name, field_dict['field_name'])
                    self.assertEqual(field_info.type, field_dict['type'])
                except Exception as e:
                    print(e)
                    print(field_dict['field_name'], field_dict['type'])
                    raise e
