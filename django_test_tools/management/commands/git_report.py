import subprocess
from django.core.management import BaseCommand

import logging

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

        # parser.add_argument("-u", "--username",
        #                 dest="usernames",
        #                 help="LDAP usernames for employees",
        #                 nargs='+',
        #                 )
        pass

    def handle(self, *args, **options):
        if options.get('format') is None:
            git_format = '%h|%ae|%ai|%s'
        else:
            git_format = options.get('format')

        git_lines = self.report(git_format)
        for line in git_lines:
            self.stdout.write(line)
        self.stdout.write('Finished processing')

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
