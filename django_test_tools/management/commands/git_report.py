import subprocess
from django.core.management import BaseCommand


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
                            help="Git forma",
                            default=None,
                            )

        # parser.add_argument("-u", "--username",
        #                 dest="usernames",
        #                 help="LDAP usernames for employees",
        #                 nargs='+',
        #                 )
        pass

    def handle(self, *args, **options):
        git_format = options.get('format', '%h|%ae|%ai|%s"')
        git_lines = self.report(git_format)
        for line in git_lines:
            self.stdout.writable(line)


    def report(self, format):
        # git log --pretty=format:"%h - %an, %ad : %s" --date=iso
        #
        # git log --pretty="%h - %s" --author=gitster --since="2008-10-01"
        # --before="2008-11-01" --no-merges -- t/
        try:
            # git-describe doesn't update the git-index, so we do that
            subprocess.check_output(["git", "update-index", "--refresh"])

            # get info about the latest tag in git
            describe_out = subprocess.check_output([
                "git",
                "log",
                '--date=iso',
                '--pretty=format:"{}"'.format(format)
            ], stderr=subprocess.STDOUT
            ).decode()
        except subprocess.CalledProcessError:
            # logger.warn("Error when running git describe")
            return {}

        return describe_out.split('\n')
