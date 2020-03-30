from django.conf import settings
from django.test import TestCase

from django_test_tools.generators.model_generator import FactoryBoyGenerator


class TestFactoryBoyGenerator(TestCase):

    def test_create_template_data_servers(self):
        generator = FactoryBoyGenerator()
        server_template_data = generator.create_template_data(settings.TEST_APP_SERVERS)
        #write_assertions(server_template_data, 'server_template_data')
        self.assertEqual(server_template_data['app_name'], 'example.servers')
        self.assertEqual(len(server_template_data['models']['operatingsystem']['fields']), 4)
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][0]['factory'],
                         'LazyAttribute(lambda x: faker.text(max_nb_chars=20))')
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][0]['field_name'], 'name')
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][0]['is_supported'], True)
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][0]['type'], 'CharField')
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][1]['factory'],
                         'LazyAttribute(lambda x: FuzzyText(length=5, chars=string.ascii_letters).fuzz())')
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][1]['field_name'], 'version')
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][1]['is_supported'], True)
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][1]['type'], 'CharField')
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][2]['factory'],
                         'LazyAttribute(lambda o: randint(3, 3))')
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][2]['field_name'],
                         'licenses_available')
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][2]['is_supported'], True)
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][2]['type'], 'IntegerField')
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][3]['factory'],
                         'LazyAttribute(lambda x: faker.pydecimal(left_digits=5, right_digits=2, positive=True))')
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][3]['field_name'], 'cost')
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][3]['is_supported'], True)
        self.assertEqual(server_template_data['models']['operatingsystem']['fields'][3]['type'], 'DecimalField')
        self.assertEqual(server_template_data['models']['operatingsystem']['model_name'], 'OperatingSystem')
        self.assertEqual(server_template_data['models']['operatingsystem']['package_name'],
                         'example.servers.OperatingSystem')
        self.assertEqual(server_template_data['models']['operatingsystem']['unique_together'], ('name', 'version'))
        self.assertEqual(len(server_template_data['models']['server']['fields']), 10)
        self.assertEqual(server_template_data['models']['server']['fields'][0]['factory'],
                         'LazyAttribute(lambda x: faker.text(max_nb_chars=20))')
        self.assertEqual(server_template_data['models']['server']['fields'][0]['field_name'], 'name')
        self.assertEqual(server_template_data['models']['server']['fields'][0]['is_supported'], True)
        self.assertEqual(server_template_data['models']['server']['fields'][0]['type'], 'CharField')
        self.assertEqual(server_template_data['models']['server']['fields'][1]['factory'],
                         'LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))')
        self.assertEqual(server_template_data['models']['server']['fields'][1]['field_name'], 'notes')
        self.assertEqual(server_template_data['models']['server']['fields'][1]['is_supported'], True)
        self.assertEqual(server_template_data['models']['server']['fields'][1]['type'], 'TextField')
        self.assertEqual(server_template_data['models']['server']['fields'][2]['factory'], 'Iterator([True, False])')
        self.assertEqual(server_template_data['models']['server']['fields'][2]['field_name'], 'virtual')
        self.assertEqual(server_template_data['models']['server']['fields'][2]['is_supported'], True)
        self.assertEqual(server_template_data['models']['server']['fields'][2]['type'], 'BooleanField')
        self.assertEqual(server_template_data['models']['server']['fields'][3]['factory'],
                         'LazyAttribute(lambda o: faker.ipv4(network=False))')
        self.assertEqual(server_template_data['models']['server']['fields'][3]['field_name'], 'ip_address')
        self.assertEqual(server_template_data['models']['server']['fields'][3]['is_supported'], True)
        self.assertEqual(server_template_data['models']['server']['fields'][3]['type'], 'GenericIPAddressField')
        self.assertEqual(server_template_data['models']['server']['fields'][4]['factory'],
                         'LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", end_date="now", tzinfo=timezone(settings.TIME_ZONE)))')
        self.assertEqual(server_template_data['models']['server']['fields'][4]['field_name'], 'created')
        self.assertEqual(server_template_data['models']['server']['fields'][4]['is_supported'], True)
        self.assertEqual(server_template_data['models']['server']['fields'][4]['type'], 'DateTimeField')
        self.assertEqual(server_template_data['models']['server']['fields'][5]['factory'],
                         'LazyAttribute(lambda x: faker.date_between(start_date="-1y", end_date="today", tzinfo=timezone(settings.TIME_ZONE)))')
        self.assertEqual(server_template_data['models']['server']['fields'][5]['field_name'], 'online_date')
        self.assertEqual(server_template_data['models']['server']['fields'][5]['is_supported'], True)
        self.assertEqual(server_template_data['models']['server']['fields'][5]['type'], 'DateField')
        self.assertEqual(server_template_data['models']['server']['fields'][6]['factory'],
                         'SubFactory(OperatingSystemFactory)')
        self.assertEqual(server_template_data['models']['server']['fields'][6]['field_name'], 'operating_system')
        self.assertEqual(server_template_data['models']['server']['fields'][6]['is_supported'], True)
        self.assertEqual(server_template_data['models']['server']['fields'][6]['type'], 'ForeignKey')
        self.assertEqual(server_template_data['models']['server']['fields'][7]['factory'],
                         'LazyAttribute(lambda x: FuzzyText(length=6, chars=string.digits).fuzz())')
        self.assertEqual(server_template_data['models']['server']['fields'][7]['field_name'], 'server_id')
        self.assertEqual(server_template_data['models']['server']['fields'][7]['is_supported'], True)
        self.assertEqual(server_template_data['models']['server']['fields'][7]['type'], 'CharField')
        self.assertEqual(server_template_data['models']['server']['fields'][8]['factory'],
                         'Iterator(((\'PROD\', \'Prod\'), (\'DEV\', \'Dev\')), getter=lambda x: x[0])')
        self.assertEqual(server_template_data['models']['server']['fields'][8]['field_name'], 'use')
        self.assertEqual(server_template_data['models']['server']['fields'][8]['is_supported'], True)
        self.assertEqual(server_template_data['models']['server']['fields'][8]['type'], 'CharField')
        self.assertEqual(server_template_data['models']['server']['fields'][9]['factory'],
                         'LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))')
        self.assertEqual(server_template_data['models']['server']['fields'][9]['field_name'], 'comments')
        self.assertEqual(server_template_data['models']['server']['fields'][9]['is_supported'], True)
        self.assertEqual(server_template_data['models']['server']['fields'][9]['type'], 'TextField')
        self.assertEqual(server_template_data['models']['server']['model_name'], 'Server')
        self.assertEqual(server_template_data['models']['server']['package_name'], 'example.servers.Server')

    def test_create_template_data_people(self):
        generator = FactoryBoyGenerator()
        people_template_data = generator.create_template_data(settings.TEST_APP_PEOPLE)
        # write_assertions(people_template_data, 'people_template_data')
        # self.fail('Running assertion')
        self.assertEqual(people_template_data['app_name'], 'example.people')
        self.assertEqual(len(people_template_data['models']['person']['fields']), 15)
        self.assertEqual(people_template_data['models']['person']['fields'][0]['factory'],
                         'LazyAttribute(lambda x: faker.text(max_nb_chars=60))')
        self.assertEqual(people_template_data['models']['person']['fields'][0]['field_name'], 'first_name')
        self.assertEqual(people_template_data['models']['person']['fields'][0]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][0]['type'], 'CharField')
        self.assertEqual(people_template_data['models']['person']['fields'][1]['factory'],
                         'LazyAttribute(lambda x: FuzzyText(length=60, chars=string.digits).fuzz())')
        self.assertEqual(people_template_data['models']['person']['fields'][1]['field_name'], 'middle_name')
        self.assertEqual(people_template_data['models']['person']['fields'][1]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][1]['type'], 'CharField')
        self.assertEqual(people_template_data['models']['person']['fields'][2]['factory'],
                         'LazyAttribute(lambda x: faker.text(max_nb_chars=60))')
        self.assertEqual(people_template_data['models']['person']['fields'][2]['field_name'], 'last_name')
        self.assertEqual(people_template_data['models']['person']['fields'][2]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][2]['type'], 'CharField')
        self.assertEqual(people_template_data['models']['person']['fields'][3]['factory'],
                         'Iterator(((\'M\', \'Male\'), (\'F\', \'Female\')), getter=lambda x: x[0])')
        self.assertEqual(people_template_data['models']['person']['fields'][3]['field_name'], 'sex')
        self.assertEqual(people_template_data['models']['person']['fields'][3]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][3]['type'], 'CharField')
        self.assertEqual(people_template_data['models']['person']['fields'][4]['factory'],
                         'LazyAttribute(lambda x: FuzzyText(length=50, chars=string.digits).fuzz())')
        self.assertEqual(people_template_data['models']['person']['fields'][4]['field_name'], 'national_id')
        self.assertEqual(people_template_data['models']['person']['fields'][4]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][4]['type'], 'CharField')
        self.assertEqual(people_template_data['models']['person']['fields'][5]['factory'],
                         'LazyAttribute(lambda o: randint(3, 3))')
        self.assertEqual(people_template_data['models']['person']['fields'][5]['field_name'], 'national_id_type')
        self.assertEqual(people_template_data['models']['person']['fields'][5]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][5]['type'], 'IntegerField')
        self.assertEqual(people_template_data['models']['person']['fields'][6]['factory'],
                         'Iterator([\'PA\', \'US\', \'GB\',])')
        self.assertEqual(people_template_data['models']['person']['fields'][6]['field_name'], 'country_for_id')
        self.assertEqual(people_template_data['models']['person']['fields'][6]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][6]['type'], 'CountryField')
        self.assertEqual(people_template_data['models']['person']['fields'][7]['field_name'], 'picture')
        self.assertEqual(people_template_data['models']['person']['fields'][7]['is_supported'], False)
        self.assertEqual(people_template_data['models']['person']['fields'][7]['type'], 'ImageField')
        self.assertEqual(people_template_data['models']['person']['fields'][8]['factory'],
                         'LazyAttribute(lambda x: faker.date_between(start_date="-1y", end_date="today", tzinfo=timezone(settings.TIME_ZONE)))')
        self.assertEqual(people_template_data['models']['person']['fields'][8]['field_name'], 'date_of_birth')
        self.assertEqual(people_template_data['models']['person']['fields'][8]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][8]['type'], 'DateField')
        self.assertEqual(people_template_data['models']['person']['fields'][9]['factory'],
                         'LazyAttribute(lambda x: FuzzyText(length=4, chars=string.ascii_letters).fuzz())')
        self.assertEqual(people_template_data['models']['person']['fields'][9]['field_name'], 'blood_type')
        self.assertEqual(people_template_data['models']['person']['fields'][9]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][9]['type'], 'CharField')
        self.assertEqual(people_template_data['models']['person']['fields'][10]['factory'],
                         'LazyAttribute(lambda x: faker.text(max_nb_chars=60))')
        self.assertEqual(people_template_data['models']['person']['fields'][10]['field_name'], 'religion')
        self.assertEqual(people_template_data['models']['person']['fields'][10]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][10]['type'], 'CharField')
        self.assertEqual(people_template_data['models']['person']['fields'][11]['factory'],
                         'FileField(filename=\'document.txt\')')
        self.assertEqual(people_template_data['models']['person']['fields'][11]['field_name'], 'document')
        self.assertEqual(people_template_data['models']['person']['fields'][11]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][11]['type'], 'FileField')
        self.assertEqual(people_template_data['models']['person']['fields'][12]['field_name'], 'salary_currency')
        self.assertEqual(people_template_data['models']['person']['fields'][12]['is_supported'], False)
        self.assertEqual(people_template_data['models']['person']['fields'][12]['type'], 'CurrencyField')
        self.assertEqual(people_template_data['models']['person']['fields'][13]['factory'],
                         'LazyAttribute(lambda x: faker.pydecimal(left_digits=12, right_digits=2, positive=True))')
        self.assertEqual(people_template_data['models']['person']['fields'][13]['field_name'], 'salary')
        self.assertEqual(people_template_data['models']['person']['fields'][13]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][13]['type'], 'MoneyField')
        self.assertEqual(people_template_data['models']['person']['fields'][14]['factory'],
                         'LazyAttribute(lambda x: faker.text(max_nb_chars=16))')
        self.assertEqual(people_template_data['models']['person']['fields'][14]['field_name'], 'cell_phone')
        self.assertEqual(people_template_data['models']['person']['fields'][14]['is_supported'], True)
        self.assertEqual(people_template_data['models']['person']['fields'][14]['type'], 'CharField')
        self.assertEqual(people_template_data['models']['person']['model_name'], 'Person')
        self.assertEqual(people_template_data['models']['person']['package_name'], 'example.people.Person')
