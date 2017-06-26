from django.test import TestCase

from django_test_tools.assert_utils import generate_assert_equals_dictionaries, write_assert_list, \
    generate_assert_equals_list
import logging

from django_test_tools.file_utils import temporary_file, hash_file

logger = logging.getLogger(__name__)
class Testgenerate_assert_equals_dictionaries(TestCase):

    def test_generate_assert_equals_dictionaries(self):
        data = [
            {'name': 'kilo', 'password': 9999, 'groups': ['admin', 'users']}
        ]
        results = generate_assert_equals_list(data, 'data')
        self.assertEqual('self.assertEqual(1, len(data))', results[0])

    @temporary_file('py', delete_on_exit=True)
    def test_write_assert_list(self):
        data = [
            {'name': 'kilo', 'password': 9999,
             'groups': ['admin', 'users'],
             'config':{'server': 'all', 'bulding': 116}},
            {'name': 'pasto', 'password': 'nogo',
             'groups': ['users'],
             'config': {'server': 'database', 'bulding': 116}}
        ]
        filename = write_assert_list(self.test_write_assert_list.filename, data, 'data')
        self.assertEqual(filename, self.test_write_assert_list.filename)
        hash_digest = hash_file(filename)
        self.assertEqual('2848cab5285d55c71f727aee4e966914f51dd4ee', hash_digest)

