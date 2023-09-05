import json
from django.core.management import BaseCommand

from ...app_manager import DjangoAppManager


class Command(BaseCommand):
    """

        $ python manage.py
    """

    def add_arguments(self, parser):
        parser.add_argument('app_name')

        parser.add_argument("-f", "--filename",
                            dest="filename",
                            help="Filename",
                            )

    def handle(self, *args, **options):
        app_name = options.get('app_name', None)
        app_manager = DjangoAppManager()
        app_data = app_manager.get_app_data(app_name)
        with open(options['filename'], 'w', encoding='utf-8') as json_file:
            json.dump(app_data, json_file, indent=4, default=str)

        self.stdout.write(f'Wrote dictionary to {options["filename"]}')
