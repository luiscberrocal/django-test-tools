import collections
from datetime import datetime, date

from decimal import Decimal

from django_test_tools.utils import create_output_filename_with_date


def write_assert_list(filename, dictionary_list, variable_name):
    """
    Function to generate assertions for a dictionary or list content.
    :param filename:
    :param dictionary_list:
    :param variable_name:
    :return:
    """
    writer = AssertionWriter()
    return writer.write_assert_list(dictionary_list, variable_name, filename=filename)


class AssertionWriter(object):

    def __init__(self, **kwargs):
        self.excluded_variable_names = ['created', 'modified']

    def write_assert_list(self, dictionary_list, variable_name, **kwargs):
        """
        Function to generate assertions for a dictionary or list content.
        :param filename:
        :param dictionary_list:
        :param variable_name:
        :return:
        """
        if kwargs.get('filename') is None:
            filename = create_output_filename_with_date('{}.py'.format(variable_name))
        else:
            filename = kwargs.get('filename')

        if isinstance(dictionary_list, dict):
            assert_list = self._generate_assert_equals_dictionaries(dictionary_list, variable_name)
        elif isinstance(dictionary_list, list):
            assert_list = self._generate_assert_equals_list(dictionary_list, variable_name)

        with open(filename, 'w', encoding='utf-8', newline='\n') as python_file:
            python_file.write('\n'.join(assert_list))

        return filename

    def _generate_assert_equals_list(self, data_list, variable_name):
        assert_list = list()
        if variable_name not in self.excluded_variable_names:
            index = 0
            # assert_list.append('# ********** variable {} ***********'.format(variable_name))
            assert_list.append('self.assertEqual({}, {})'.format(len(data_list), 'len({})'.format(variable_name)))
            for data in data_list:
                list_variable = '{}[{}]'.format(variable_name, index)
                self._build_assertion(list_variable, data, assert_list)
                index += 1
        return assert_list

    def _generate_assert_equals_dictionaries(self, dictionary, variable_name):
        assert_list = list()
        if variable_name not in self.excluded_variable_names:
            ordered_dictionary = collections.OrderedDict(sorted(dictionary.items()))
            for key, value in ordered_dictionary.items():
                if key not in self.excluded_variable_names:
                    dict_variable = '{}[\'{}\']'.format(variable_name, key)
                    self._build_assertion(dict_variable, value, assert_list)
        return assert_list

    def _build_assertion(self, variable_name, data, assert_list):
        if variable_name not in self.excluded_variable_names:
            if isinstance(data, str):
                assert_list.append('self.assertEqual(\'{}\', {})'.format(data, variable_name))
            elif isinstance(data, datetime):
                date_time_format = '%Y-%m-%d %H:%M:%S%z'
                str_datetime = data.strftime(date_time_format)
                assert_list.append(
                    'self.assertEqual(\'{}\', {}.strftime(\'{}\'))'.format(str_datetime, variable_name, date_time_format))
            elif isinstance(data, date):
                date_format = '%Y-%m-%d'
                str_date = data.strftime(date_format)
                assert_list.append(
                    'self.assertEqual(\'{}\', {}.strftime(\'{}\'))'.format(str_date, variable_name, date_format))
            elif isinstance(data, Decimal):
                assert_list.append('self.assertEqual(Decimal({}), {})'.format(data, variable_name))
            elif isinstance(data, list):
                assert_list += self._generate_assert_equals_list(data, variable_name)
            elif isinstance(data, dict):
                assert_list += self._generate_assert_equals_dictionaries(data, variable_name)
            else:
                assert_list.append('self.assertEqual({}, {})'.format(data, variable_name))



