from django.core.management import BaseCommand


class Command(BaseCommand):
    """
        $ python manage.py
    """

    def add_arguments(self, parser):
        # parser.add_argument('requirement_filename')
        # parser.add_argument("-l", "--list",
        #                     action='store_true',
        #                     dest="list",
        #                     help="List data",
        #                     )

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
        pass

    def handle(self, *args, **options):
        pass
