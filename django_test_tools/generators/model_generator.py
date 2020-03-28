from ..app_manager import DjangoAppManager


class FactoryBoyGenerator(object):

    def __init__(self, **kwargs):
        self.app_manager = DjangoAppManager()
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
        self.read_only_fields = ['AutoField', 'AutoCreatedField', 'AutoLastModifiedField']
        self.fields_to_ignore = []
        self.default_countries = kwargs.get('default_countries', ['PA', 'US', 'GB'])

    def create_template_data(self, app_name):
        app_data = self.app_manager.get_app_data(app_name)
        template_data = dict()
        template_data['models'] = dict()
        template_data['app_name'] = app_data['app_name']
        for model_key in app_data['models'].keys():
            template_data['models'][model_key] = dict()
            template_data['models'][model_key]['model_name'] = app_data['models'][model_key]['model_name']
            template_data['models'][model_key]['package_name'] = '{}.{}'.format(app_data['app_name'],
                                                                                app_data['models'][model_key][
                                                                                    'model_name'])
            template_data['models'][model_key]['fields'] = list()

            for field in app_data['models'][model_key]['fields']:
                field_dict = dict()
                field_dict['field_name'] = field['field_name']
                field_dict['type'] = field['type']
                field_dict['is_supported'] = True
                if field['type'] in self.read_only_fields or field['type'] in self.fields_to_ignore:
                    pass
                elif field['type'].lower()  == 'charfield':
                    field_dict['factory'] = self.get_charfield_factory(field)
                    template_data['models'][model_key]['fields'].append(field_dict)
                elif field['type'] == 'DateTimeField':
                    config = {'start_date': '-1y', 'end_date': 'now'}
                    template = 'LazyAttribute(lambda x: faker.date_time_between(start_date="{start_date}", ' \
                               'end_date="{end_date}", tzinfo=timezone(settings.TIME_ZONE)))'
                    field_dict['factory'] = template.format(**config)
                    template_data['models'][model_key]['fields'].append(field_dict)
                elif field['type'] == 'ForeignKey':
                    template = 'SubFactory({model_name}Factory)'
                    field_dict['factory'] = template.format(**template_data['models'][model_key])
                    template_data['models'][model_key]['fields'].append(field_dict)
                elif field['type'].lower() == 'countryfield':
                    country_list_str = ''
                    for country in self.default_countries:
                        country_list_str += '\'{}\''.format(country)
                    template = 'Iterator([{}])'
                    field_dict['factory'] = template.format(country_list_str)
                    template_data['models'][model_key]['fields'].append(field_dict)
                elif field['type'].lower() == 'booleanfield':
                    field_dict['factory'] = self.get_booleanfield_factory(field)
                    template_data['models'][model_key]['fields'].append(field_dict)
                elif field['type'].lower() == 'textfield':
                    field_dict['factory'] = self.get_textfield_factory(field)
                    template_data['models'][model_key]['fields'].append(field_dict)
                elif field['type'].lower() == 'integerfield':
                    field_dict['factory'] = self.get_integerfield_factory(field)
                    template_data['models'][model_key]['fields'].append(field_dict)
                elif field['type'].lower() == 'filefield':
                    field_dict['factory'] = self.get_filefield_factory(field)
                    template_data['models'][model_key]['fields'].append(field_dict)
                #     field_data = {'print': PRINT_FILEFIELD, 'args': [field.name, field.name, 'xlsx']}
                #     factory_class_content.append(field_data)
                #
                # elif field['type'].lower()  == 'decimalfield' or field['type'].lower()  == 'moneyfield':
                #     max_left = field.max_digits - field.decimal_places
                #     max_right = field.decimal_places
                #     field_data = {'print': PRINT_DECIMALFIELD,
                #                   'args': [field.name, max_left, max_right]}
                #     factory_class_content.append(field_data)
                #
                # elif field['type'].lower()  == 'genericipaddressfield':
                #     field_data = {'print': PRINT_IPADDRESSFIELD, 'args': [field.name]}
                #     factory_class_content.append(field_data)
                else:
                    field_dict['is_supported'] = False
                    template_data['models'][model_key]['fields'].append(field_dict)
        return template_data

    def get_booleanfield_factory(self, *args, **kwargs):
        return 'Iterator([True, False])'

    def get_textfield_factory(self, *args, **kwargs):
        config = {'sentences': kwargs.get('sentences', 3)}
        template = 'LazyAttribute(lambda x: faker.paragraph(nb_sentences={sentences}, variable_nb_sentences=True))'
        return template.format(**config)

    def get_integerfield_factory(self, *args, **kwargs):
        config = {'min_value': kwargs.get('min_value', 3),
                  'max_value': kwargs.get('max_value', 3), }
        template = 'LazyAttribute(lambda o: randint({min_value}, {max_value}))'
        return template.format(**config)

    def get_filefield_factory(self, *args, **kwargs):
        config = {'filename': kwargs.get('filename', args[0]['field_name']),
                  'extension': kwargs.get('extension', 'txt'), }
        template = 'FileField(filename=\'{}.{}\''
        return template.format(**config)

    def get_charfield_factory(self, *args, **kwargs):
        config = {'filename': kwargs.get('filename', args[0]['field_name']),
                  'extension': kwargs.get('extension', 'txt'), }
        template = 'LazyAttribute(lambda x: faker.text(max_nb_chars={max_length}))'
        return template.format(**args[0])
