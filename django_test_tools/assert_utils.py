import collections
from datetime import datetime, date
from decimal import Decimal

from openpyxl.compat import deprecated

from .re.regexp import CommonRegExp
from .utils import create_output_filename_with_date


def write_assertions(dictionary_list, variable_name, **kwargs):
    """
    Writes assertions using Django practice of putting actual value first and then expected value to a file.
    If no filename is supplied it will generate a file in the settings.TEST_OUTPUT_PATH folder with the
    **variable_name** and the current date.
    By default key named created and modified will be excluded.

    :param dictionary_list: dictionary or list of values
    :param variable_name: name of the variable
    :param kwargs: filename String. Full path to the output file.
    :param kwargs: excluded_keys list of strings. List with keys to exclude
    :return: filename string.
    """
    writer = AssertionWriter(excluded_keys=kwargs.get('excluded_keys'))
    return writer.write_assert_list(dictionary_list, variable_name, filename=kwargs.get('filename'))


@deprecated('Use assert_utils.write_assertions instead')
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
    """
    This class generates assertions using Django practice of putting actual value first and then expected value.
    """
    def __init__(self, **kwargs):
        self.excluded_variable_names = ['created', 'modified']
        if kwargs.get('excluded_keys') is not None:
            for key in kwargs.get('excluded_keys'):
                self.excluded_variable_names.append(key)

        self.use_regexp_assertion = kwargs.get('use_regexp_assertion', False)
        if self.use_regexp_assertion:
            self.common_regexp = CommonRegExp(strict=True)

    def add_regular_expression(self, name, pattern, **kwargs):
        self.common_regexp.add_regular_expression(name, pattern, **kwargs)

    def write_assert_list(self, dictionary_list, variable_name, **kwargs):
        """
        Function to generate assertions for a dictionary or list content.
        :param kwargs:
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

    def _generate_assert_equals_list(self, data_list, variable_name, indentation_level=0):
        assert_list = list()
        if variable_name not in self.excluded_variable_names:
            index = 0
            # assert_list.append('# ********** variable {} ***********'.format(variable_name))
            assert_list.append('self.assertEqual({}, {})'.format('len({})'.format(variable_name), len(data_list)))
            for data in data_list:
                list_variable = '{}[{}]'.format(variable_name, index)
                self._build_assertion(list_variable, data, assert_list)
                index += 1
        return assert_list

    def _generate_assert_equals_dictionaries(self, dictionary, variable_name, **kwargs):
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
                data = data.translate(str.maketrans({"'":'\\\''}))
                if self.use_regexp_assertion:
                    pattern = self.common_regexp.match_regexp(data)[0]
                    if pattern is None:
                        assert_list.append('self.assertEqual({}, \'{}\')'.format(variable_name, data))
                    else:
                        assert_list.append('self.assertRegex({}, r\'{}\')'.format(variable_name, pattern))
                else:
                    assert_list.append('self.assertEqual({}, \'{}\')'.format(variable_name, data))
            elif isinstance(data, datetime):
                date_time_format = '%Y-%m-%d %H:%M:%S%z'
                str_datetime = data.strftime(date_time_format)
                assert_list.append(
                    'self.assertEqual({}.strftime(\'{}\'), \'{}\')'.format(
                        variable_name,
                        date_time_format,
                        str_datetime,
                    )
                )
            elif isinstance(data, date):
                date_format = '%Y-%m-%d'
                str_date = data.strftime(date_format)
                assert_list.append(
                    'self.assertEqual({}.strftime(\'{}\'), \'{}\')'.format(variable_name, date_format, str_date))
            elif isinstance(data, Decimal):
                assert_list.append('self.assertEqual({}, Decimal({}))'.format(variable_name, data))
            elif isinstance(data, list):
                assert_list += self._generate_assert_equals_list(data, variable_name)
            elif isinstance(data, dict):
                assert_list += self._generate_assert_equals_dictionaries(data, variable_name)
            else:
                assert_list.append('self.assertEqual({}, {})'.format(variable_name, data))




