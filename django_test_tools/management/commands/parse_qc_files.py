import os

from django.core.management import BaseCommand

from ...file_utils import add_date
from ...flake8.parsers import Flake8Parser, RadonParser


class Command(BaseCommand):
    """

        $ python manage.py
    """

    def add_arguments(self, parser):
        parser.add_argument("-m", "--mode", dest="mode", default="FLAKE8", help="FLAKE8 or RADON")
        parser.add_argument("-i", "--input", dest="input_file", help="Input file")
        parser.add_argument("-o", "--output", dest="output_file", help="Output file")

        # parser.add_argument('output_filename')
        # parser.add_argument("-l", "--list",
        #                     action='store_true',
        #                     dest="list",
        #                     help="List employees",
        #                     )
        # parser.add_argument("-a", "--assign",
        #                     action='store_true',
        #                     dest="assign",
        #                     help="Create unit assignments",
        #                     )
        #
        # parser.add_argument("--office",
        #                     dest="office",
        #                     help="Organizational unit short name",
        #                     default=None,
        #                     )
        # parser.add_argument("--start-date",
        #                     dest="start_date",
        #                     help="Start date for the assignment",
        #                     default=None,
        #                     )
        # parser.add_argument("--fiscal-year",
        #                     dest="fiscal_year",
        #                     help="Fiscal year for assignments",
        #                     default=None,
        #                     )
        # parser.add_argument("-u", "--username",
        #                 dest="usernames",
        #                 help="LDAP usernames for employees",
        #                 nargs='+',
        #                 )

    def handle(self, *args, **options):
        if not options.get('output_file'):
            output_filename = add_date(options.get('input_file'))
            filename, file_extension = os.path.splitext(output_filename)
            if file_extension != 'csv':
                output_filename = '{}.csv'.format(filename)
        else:
            output_filename = options.get('output_file')

        if options.get('mode') == 'FLAKE8':
            parser = Flake8Parser()
            parser.write_summary(options['input_file'], output_filename)
        elif options.get('mode') == 'RADON':
            parser = RadonParser()
            parser.write_totals(options['input_file'], output_filename)

        self.stdout.write('mode {}'.format(options.get('mode')))
        self.stdout.write('input: {}'.format(options.get('input_file')))
        self.stdout.write('output: {}'.format(output_filename))
