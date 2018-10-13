import os

import subprocess
from django.conf import settings
from django.core.management import BaseCommand

import logging
from openpyxl import Workbook

from django_test_tools.file_utils import add_date

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    git log --pretty="format:%h|%ae|%ai|%s" > ./output/commits.txt


        $ python manage.py git_report
    """

    def add_arguments(self, parser):
        # parser.add_argument('requirement_filename')
        # parser.add_argument("-l", "--list",
        #                     action='store_true',
        #                     dest="list",
        #                     help="List data",
        #                     )

        parser.add_argument("--format",
                            dest="format",
                            help="Git format",
                            default=None,
                            )

        parser.add_argument('-f', "--filename",
                            dest="filename",
                            help="Output filename",
                            default=None,
                            )

        # parser.add_argument("-u", "--username",
        #                 dest="usernames",
        #                 help="LDAP usernames for employees",
        #                 nargs='+',
        #                 )

    def handle(self, *args, **options):
        headers = ['Hash', 'Email', 'Date', 'Description']
        if options.get('format') is None:
            git_format = '%h|%ae|%ai|%s'
        else:
            git_format = options.get('format')

        if options.get('filename') is None:
            filepath = os.path.join(settings.TEST_OUTPUT_PATH, 'gir_report.xlsx')
            filename = add_date(filepath)
        else:
            filename = options.get('filename')

        wb = Workbook()
        sheet = wb.create_sheet()
        row = 1
        col = 1
        for header in headers:
            sheet.cell(row=row, column=col, value=header)
            col += 1
        row += 1
        git_lines = self.report(git_format)
        for line in git_lines:
            self.stdout.write(line)
            line_data = line.split('|')
            col = 1
            for data in line_data:
                sheet.cell(row=row, column=col, value=data)
                col += 1
            row += 1

        wb.save(filename)

        self.stdout.write('Finished processing {}'.format(filename))

    def report(self, git_format):
        # git log --pretty=format:"%h - %an, %ad : %s" --date=iso
        #
        # git log --pretty="%h - %s" --author=gitster --since="2008-10-01"
        # --before="2008-11-01" --no-merges -- t/
        try:
            # git-describe doesn't update the git-index, so we do that
            # subprocess.check_output(["git", "update-index", "--refresh"])

            # get info about the latest tag in git
            git_commands = ["git", "log", '--date=iso', '--pretty=format:"{}"'.format(git_format)]

            describe_out = subprocess.check_output(
                git_commands,
                stderr=subprocess.STDOUT
            ).decode()
        except subprocess.CalledProcessError:
            logger.warning("Error when running git describe")
            return {}

        return describe_out.split('\n')
