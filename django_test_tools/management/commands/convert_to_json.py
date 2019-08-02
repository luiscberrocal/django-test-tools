import os

import json
from django.conf import settings
from django.core.management import BaseCommand

from django_test_tools.excel import ExcelAdapter
from django_test_tools.file_utils import add_date, create_dated


class Command(BaseCommand):
    """
        $ python manage.py -i path/to/excel.xlsx -d ./output/
    """

    def add_arguments(self, parser):
        # parser.add_argument('requirement_filename')
        parser.add_argument("-i", "--input",
                            dest="input",
                            help="Input Excel file",
                            )

        parser.add_argument("-o", "--output",
                            dest="output",
                            help="Output filename",
                            )

        # parser.add_argument("--office",
        #                     dest="office",
        #                     help="Organizational unit short name",
        #                     default=None,
        #                     )

        # parser.add_argument("-u", "--username",
        #                 dest="usernames",
        #                 help="LDAP usernames for employees",
        #                 nargs='+',
        #                 )

    def handle(self, *args, **options):
        dict_data = ExcelAdapter.convert_to_dict(options['input'])
        out_file = options.get('output', create_dated('excel_to_json.json'))
        with open(out_file, 'w') as json_file:
            json.dump(dict_data, json_file, indent=4)

        self.stdout.write('Wrote {}'.format(out_file))
