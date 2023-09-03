import json

from django.conf import settings
from django.test import TestCase

from django_test_tools.app_manager import DjangoAppManager


class TestDjangoAppManager(TestCase):
    def test_installed_apps(self):
        app_manager = DjangoAppManager()
        self.assertEqual(9, len(app_manager.installed_apps))

    def test_get_app_1(self):
        app_manager = DjangoAppManager()
        app = app_manager.get_app(settings.TEST_APP_SERVERS)
        self.assertEqual(settings.TEST_APP_SERVERS, app.name)
        self.assertEqual('example.servers', app.name)
        self.assertEqual(app.models['server'].__name__, 'server')
        self.assertEqual(len(app.models['server']._meta.fields), 11)
        self.assertEqual(app.models['server']._meta.fields[0].name, 'id')
        self.assertEqual(type(app.models['server']._meta.fields[0].name).__name__, 'id')

    def test_get_project_apps(self):
        app_manager = DjangoAppManager()
        app_module = settings.TEST_APP_SERVERS.split('.')[0]
        apps = app_manager.get_project_apps(app_module)
        self.assertEqual(2, len(apps))
        apps = app_manager.get_project_apps('django')
        self.assertEqual(6, len(apps))

    def test_get_app(self):
        app_manager = DjangoAppManager()
        app_dict = app_manager.get_app_data(settings.TEST_APP_PEOPLE)

        from pathlib import Path
        filename = Path(settings.TEST_OUTPUT_PATH) / 'people_models.json'
        with open(filename, 'w') as f:
            json.dump(app_dict, f, indent=4, default=str)

        self.assertEqual(app_dict['app_name'], 'example.people')
        self.assertEqual(len(app_dict['models']['person']['fields']), 18)
        self.assertEqual(app_dict['models']['person']['fields'][0]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][0]['field_name'], 'id')
        self.assertEqual(app_dict['models']['person']['fields'][0]['type'], 'AutoField')
        self.assertEqual(app_dict['models']['person']['fields'][0]['unique'], True)
        self.assertEqual(app_dict['models']['person']['fields'][1]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][1]['field_name'], 'first_name')
        self.assertEqual(app_dict['models']['person']['fields'][1]['max_length'], 60)
        self.assertEqual(app_dict['models']['person']['fields'][1]['type'], 'CharField')
        self.assertEqual(app_dict['models']['person']['fields'][1]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][2]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][2]['field_name'], 'middle_name')
        self.assertEqual(app_dict['models']['person']['fields'][2]['max_length'], 60)
        self.assertEqual(app_dict['models']['person']['fields'][2]['type'], 'CharField')
        self.assertEqual(app_dict['models']['person']['fields'][2]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][3]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][3]['field_name'], 'last_name')
        self.assertEqual(app_dict['models']['person']['fields'][3]['max_length'], 60)
        self.assertEqual(app_dict['models']['person']['fields'][3]['type'], 'CharField')
        self.assertEqual(app_dict['models']['person']['fields'][3]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][4]['choices'], (('M', 'Male'), ('F', 'Female')))
        self.assertEqual(app_dict['models']['person']['fields'][4]['choices_type'], 'tuple')
        self.assertEqual(app_dict['models']['person']['fields'][4]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][4]['field_name'], 'sex')
        self.assertEqual(app_dict['models']['person']['fields'][4]['max_length'], 1)
        self.assertEqual(app_dict['models']['person']['fields'][4]['type'], 'CharField')
        self.assertEqual(app_dict['models']['person']['fields'][4]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][5]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][5]['field_name'], 'national_id')
        self.assertEqual(app_dict['models']['person']['fields'][5]['max_length'], 50)
        self.assertEqual(app_dict['models']['person']['fields'][5]['type'], 'CharField')
        self.assertEqual(app_dict['models']['person']['fields'][5]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][6]['choices'],
                         ((1, 'National Id'), (2, 'Drivers License'), (3, 'Passport'), (4, 'Other')))
        self.assertEqual(app_dict['models']['person']['fields'][6]['choices_type'], 'tuple')
        self.assertEqual(app_dict['models']['person']['fields'][6]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][6]['field_name'], 'national_id_type')
        self.assertEqual(app_dict['models']['person']['fields'][6]['type'], 'IntegerField')
        self.assertEqual(app_dict['models']['person']['fields'][6]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][7]['choices_type'], 'Countries')
        self.assertEqual(app_dict['models']['person']['fields'][7]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][7]['field_name'], 'country_for_id')
        self.assertEqual(app_dict['models']['person']['fields'][7]['max_length'], 2)
        self.assertEqual(app_dict['models']['person']['fields'][7]['type'], 'CountryField')
        self.assertEqual(app_dict['models']['person']['fields'][7]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][8]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][8]['field_name'], 'picture')
        self.assertEqual(app_dict['models']['person']['fields'][8]['max_length'], 100)
        self.assertEqual(app_dict['models']['person']['fields'][8]['type'], 'ImageField')
        self.assertEqual(app_dict['models']['person']['fields'][8]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][9]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][9]['field_name'], 'date_of_birth')
        self.assertEqual(app_dict['models']['person']['fields'][9]['type'], 'DateField')
        self.assertEqual(app_dict['models']['person']['fields'][9]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][10]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][10]['field_name'], 'blood_type')
        self.assertEqual(app_dict['models']['person']['fields'][10]['max_length'], 4)
        self.assertEqual(app_dict['models']['person']['fields'][10]['type'], 'CharField')
        self.assertEqual(app_dict['models']['person']['fields'][10]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][11]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][11]['field_name'], 'religion')
        self.assertEqual(app_dict['models']['person']['fields'][11]['max_length'], 60)
        self.assertEqual(app_dict['models']['person']['fields'][11]['type'], 'CharField')
        self.assertEqual(app_dict['models']['person']['fields'][11]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][12]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][12]['field_name'], 'document')
        self.assertEqual(app_dict['models']['person']['fields'][12]['max_length'], 100)
        self.assertEqual(app_dict['models']['person']['fields'][12]['type'], 'FileField')
        self.assertEqual(app_dict['models']['person']['fields'][12]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][13]['choices_type'], 'list')
        self.assertEqual(app_dict['models']['person']['fields'][13]['editable'], False)
        self.assertEqual(app_dict['models']['person']['fields'][13]['field_name'], 'salary_currency')
        self.assertEqual(app_dict['models']['person']['fields'][13]['max_length'], 3)
        self.assertEqual(app_dict['models']['person']['fields'][13]['type'], 'CurrencyField')
        self.assertEqual(app_dict['models']['person']['fields'][13]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][14]['decimal_places'], 2)
        self.assertEqual(app_dict['models']['person']['fields'][14]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][14]['field_name'], 'salary')
        self.assertEqual(app_dict['models']['person']['fields'][14]['max_digits'], 14)
        self.assertEqual(app_dict['models']['person']['fields'][14]['type'], 'MoneyField')
        self.assertEqual(app_dict['models']['person']['fields'][14]['unique'], False)
        self.assertEqual(app_dict['models']['person']['fields'][15]['editable'], True)
        self.assertEqual(app_dict['models']['person']['fields'][15]['field_name'], 'cell_phone')
        self.assertEqual(app_dict['models']['person']['fields'][15]['max_length'], 16)
        self.assertEqual(app_dict['models']['person']['fields'][15]['type'], 'CharField')
        self.assertEqual(app_dict['models']['person']['fields'][15]['unique'], False)
        self.assertEqual(app_dict['models']['person']['model_name'], 'Person')
        self.assertEqual(app_dict['models']['person']['original_attrs']['abstract'], False)

    def test_servers(self):
        app_manager = DjangoAppManager()
        app_dict = app_manager.get_app_data(settings.TEST_APP_SERVERS)

        from pathlib import Path
        filename = Path(settings.TEST_OUTPUT_PATH) / 'servers_models.json'
        with open(filename, 'w') as f:
            json.dump(app_dict, f, indent=4, default=str)
