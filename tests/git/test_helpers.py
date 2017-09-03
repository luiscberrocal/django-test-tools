import subprocess
from functools import partial
from os import environ

from django.test import TestCase

from django_test_tools.file_utils import TemporaryFolder
from django_test_tools.git.helpers import Git

SUBPROCESS_ENV = dict(
    list(environ.items()) + [(b'HGENCODING', b'utf-8')]
)

call = partial(subprocess.call, env=SUBPROCESS_ENV)
check_call = partial(subprocess.check_call, env=SUBPROCESS_ENV)
check_output = partial(subprocess.check_output, env=SUBPROCESS_ENV)


class GitTest(TestCase):
    def test_report(self):
        vcs = 'git'
        with TemporaryFolder('test_report') as temp_folder:
            temp_folder.write('somesource.txt', ['Test Data'])
            check_call([vcs, "init"])
            check_call([vcs, "add", "somesource.txt"])
            check_call([vcs, "commit", "-m", "initial commit"])
            check_call([vcs, "tag", "v1.7.2013"])

            git = Git()
            result = git.report()
        self.assertEqual(1, len(result))
        self.assertEqual(5, len(result[0].split('|')))
