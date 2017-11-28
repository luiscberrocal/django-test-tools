from django.test import SimpleTestCase

from django_test_tools.re.regexp import CommonRegExp


class TestCommonRegExp(SimpleTestCase):

    def test_match_regexp(self):
        str_data = '10:45'
        common_regexp = CommonRegExp()
        regular_expression, key = common_regexp.match_regexp(str_data)
        self.assertEqual(regular_expression, '([0-1][0-9]|2[0-4]):([0-5][0-9])')
        self.assertEqual(key, 'time_military')

    def test_add_regular_expression(self):
        str_data = 'KILOVATIO'

        common_regexp = CommonRegExp()
        common_regexp.add_regular_expression('constant', r'[A-Z]+')
        regular_expression, key = common_regexp.match_regexp(str_data)

        self.assertEqual(regular_expression, '[A-Z]+')
        self.assertEqual(key, 'constant')

    def test_add_regular_expression_strict(self):
        str_data = 'KILOVATIO'

        common_regexp = CommonRegExp(strict=True)
        common_regexp.add_regular_expression('constant', r'[A-Z]+')
        regular_expression, key = common_regexp.match_regexp(str_data)

        self.assertEqual(regular_expression, '^[A-Z]+$')
        self.assertEqual(key, 'constant')

    def test_add_regular_expression_strict(self):
        str_data = 'snake_case'

        common_regexp = CommonRegExp(strict=True)
        common_regexp.add_regular_expression('snake_case', r'^[a-z_]+$')
        regular_expression, key = common_regexp.match_regexp(str_data)

        self.assertEqual(regular_expression, '^[a-z_]+$')
        self.assertEqual(key, 'snake_case')


    def test_add_regular_expression_strict2(self):
        str_data = 'KILOVATIO'

        common_regexp = CommonRegExp()
        common_regexp.add_regular_expression('constant', r'[A-Z]+', strict=True)
        regular_expression, key = common_regexp.match_regexp(str_data)

        self.assertEqual(regular_expression, '^[A-Z]+$')
        self.assertEqual(key, 'constant')

