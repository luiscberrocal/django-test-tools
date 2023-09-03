from openpyxl.compat import deprecated

from django_test_tools.assert_utils import AssertionWriter


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
