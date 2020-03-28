from django.apps.registry import apps


class DjangoAppManager(object):
    def __init__(self):
        self.installed_apps = dict(self.get_installed_apps())

    def get_app(self, app_name):
        return self.installed_apps.get(app_name)

    def get_installed_apps(self):
        for app_config in apps.get_app_configs():
            yield app_config.name, app_config

    def get_model(self, app_name, model_name):
        app = self.get_app(app_name)
        for model in app.get_models():
            if model_name == model.__name__:
                return model
        return None

    def get_project_apps(self, project_name):
        project_apps = dict()
        for app_name, app_config in self.installed_apps.items():
            app_project = app_name.split('.')[0]
            if app_project == project_name:
                project_apps[app_name] = app_config
        return project_apps

    def get_app_data(self, app_name):
        """
        Read application data converts into a dictionary

        :param app_name: Application name
        :return: Dictionary with application data
        """
        app = self.get_app(app_name)
        app_dict = dict()
        app_dict['app_name'] = app.name
        app_dict['models'] = dict()
        for key, model in app.models.items():
            app_dict['models'][key] = dict()
            app_dict['models'][key]['model_name'] = model.__name__
            app_dict['models'][key]['original_attrs'] = model._meta.original_attrs
            app_dict['models'][key]['fields'] = list()
            for field in model._meta.fields:
                field_dict = dict()
                field_dict['field_name'] = field.name
                field_dict['type'] = type(field).__name__
                field_dict['unique'] = field.unique
                field_dict['editable'] = field.editable
                if hasattr(field, 'choices') and field.choices is not None:
                    field_dict['choices'] = field.choices
                if hasattr(field, 'max_length') and field.max_length is not None:
                    field_dict['max_length'] = field.max_length
                if hasattr(field, 'max_digits') and field.max_digits is not None:
                    field_dict['max_digits'] = field.max_digits
                if hasattr(field, 'decimal_places') and field.decimal_places is not None:
                    field_dict['decimal_places'] = field.decimal_places
                if hasattr(field, 'remote_field') and field.remote_field is not None:
                    field_dict['remote_field'] = field.remote_field.model.__name__


                app_dict['models'][key]['fields'].append(field_dict)
        return app_dict

