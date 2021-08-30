from django_test_tools.generators.base import TemplateDataParser


class FactoryBoyTemplateDataParser(TemplateDataParser):

    def parse_data(self, app_data: dict) -> dict:
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
            if app_data['models'][model_key].get('original_attrs'):
                if app_data['models'][model_key].get('original_attrs').get('unique_together'):
                    template_data['models'][model_key]['unique_together'] = app_data['models'][model_key].get(
                        'original_attrs').get('unique_together')

            for field in app_data['models'][model_key]['fields']:
                field_dict = dict()
                field_dict['field_name'] = field['field_name']
                field_dict['type'] = field['type']
                field_dict['is_supported'] = True
                if field['type'] in self.read_only_fields or field['type'] in self.fields_to_ignore:
                    pass
                else:
                    method_name = 'get_{}_factory'.format(field['type'].lower())
                    if hasattr(self, method_name):
                        field_dict['factory'] = getattr(self, method_name)(field, template_data['models'][model_key])
                        template_data['models'][model_key]['fields'].append(field_dict)
                    else:
                        field_dict['is_supported'] = False
                        template_data['models'][model_key]['fields'].append(field_dict)
        return template_data

