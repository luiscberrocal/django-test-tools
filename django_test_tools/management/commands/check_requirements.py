from django.core.management import BaseCommand

import pip

import contextlib

@contextlib.contextmanager
def capture():
    import sys
    from io import StringIO
    oldout,olderr = sys.stdout, sys.stderr
    try:
        out=[StringIO(), StringIO()]
        sys.stdout,sys.stderr = out
        yield out
    finally:
        sys.stdout,sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()

def read_requirement_file(req_file):
    for item in pip.req.parse_requirements(req_file, session="somesession"):
        print("")
        if isinstance(item, pip.req.InstallRequirement):
            print("required package: {}".format(item.name))

            if len(str(item.req.specifier)) > 0:
                print("  >>" + str(item.req.specifier))

            if item.link is not None:
                print("  from: " + item.link.url)
                print("  filename: " + item.link.filename)
                print("  egg: " + item.link.egg_fragment)

            if len(item.options) > 0:
                for opt_type,opts in item.options.iteritems():
                    print("  {}:".format(opt_type))
                    if type(opts) is list:
                        for opt in opts:
                            print("    " + opt)
                    elif type(opts) is dict:
                        for k,v in opts.iteritems():
                            print("    {}: {}".format(k,v))


class Command(BaseCommand):
    """
        $ python manage.py
    """

    def add_arguments(self, parser):
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
        pass

    def handle(self, *args, **options):
        # with capture() as out:
        #     pip.main(['list', '--outdated'])
        # for t in out:
        #     self.stdout.write(t)

        filename = r'/Users/lberrocal/PycharmProjects/django-test-tools/requirements_dev.txt'
        read_requirement_file(filename)



