import collections

from django_test_tools.utils import create_output_filename_with_date

def generate_assert_equals_list(data_list, variable_name):
    assert_list = list()
    index = 0
    #assert_list.append('# ********** variable {} ***********'.format(variable_name))
    assert_list.append('self.assertEqual({}, {})'.format(len(data_list), 'len({})'.format(variable_name)))
    for data in data_list:
        list_variable = '{}[{}]'.format(variable_name, index)
        if isinstance(data, str):
            assert_list.append('self.assertEqual(\'{}\', {})'.format(data, list_variable))
        elif isinstance(data, list):
            assert_list += generate_assert_equals_list(data, list_variable)
        elif isinstance(data, dict):
            assert_list += generate_assert_equals_dictionaries(data, list_variable)
        else:
            assert_list.append('self.assertEqual({}, {})'.format(data, list_variable))
        index += 1
    return  assert_list

def generate_assert_equals_dictionaries(dictionary, variable_name):
    assert_list = list()
    ordered_dictionary = collections.OrderedDict(sorted(dictionary.items()))
    for key, value in ordered_dictionary.items():
        dict_variable = '{}[\'{}\']'.format(variable_name, key)
        if isinstance(value, str):
            assert_list.append('self.assertEqual(\'{}\', {})'.format(value, dict_variable))
        elif isinstance(value, list):
            assert_list += generate_assert_equals_list(value, dict_variable)
        elif isinstance(value, dict ):
            assert_list += generate_assert_equals_dictionaries(value, dict_variable)
        else:
            assert_list.append('self.assertEqual({}, {})'.format(value, dict_variable))
    return assert_list


def write_assert_list(filename, dictionary_list, variable_name):
    """
    Function to generate assertions for a dictionary or list content.
    :param filename:
    :param dictionary_list:
    :param variable_name:
    :return:
    """
    if filename is None:
        filename = create_output_filename_with_date('{}.py'.format(variable_name))
    if isinstance(dictionary_list, dict):
        assert_list = generate_assert_equals_dictionaries(dictionary_list, variable_name)
    elif isinstance(dictionary_list, list):
        assert_list = generate_assert_equals_list(dictionary_list, variable_name)

    with open(filename, 'w', encoding='utf-8') as python_file:
        python_file.write('\n'.join(assert_list))
    return filename



