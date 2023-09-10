import functools
import os
import warnings

from django.conf import settings
from django.utils import timezone

from django_test_tools.file_utils import add_date
from django_test_tools.utils import weekdays


def deprecated(func):
    '''This is a decorator which can be used to mark functions
        as deprecated. It will result in a warning being emitted
        when the function is used.
       from: https://wiki.python.org/moin/PythonDecoratorLibrary#CA-92953dfd597a5cffc650d5a379452bb3b022cdd0_7
    '''

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn_explicit("Call to deprecated function {}.".format(func.__name__),
                               category=DeprecationWarning,
                               filename=func.__code__.co_filename,
                               lineno=func.__code__.co_firstlineno + 1
                               )
        return func(*args, **kwargs)

    return new_func


@deprecated
def daterange(start_date, end_date):
    """
    DEPRECATED use utils.weekdays() function instead
    :param start_date:
    :param end_date:
    :return:
    """
    return weekdays(start_date, end_date)


def create_output_filename_with_date(filename):
    """
    Based on the filename will create a full path filename incluidn the date and time in '%Y%m%d_%H%M' format.
    The path to the filename will be set in the TEST_OUTPUT_PATH settings variable.

    :param filename: base filename. my_excel_data.xlsx for example
    :return: string, full path to file with date and time in the TEST_OUTPUT_PATH folder
    """
    if getattr(settings, 'TEST_OUTPUT_PATH', None) is None:
        msg = 'You need a the variable TEST_OUTPUT_PATH in settings. It should point to a folder' \
              'for temporary data to be written and reviewed.'
        raise ValueError(msg)
    if not os.path.exists(settings.TEST_OUTPUT_PATH):
        os.makedirs(settings.TEST_OUTPUT_PATH)
    return add_date(os.path.join(settings.TEST_OUTPUT_PATH, filename))


def add_date_to_filename(filename, **kwargs):
    """
    Adds to a filename the current date and time in '%Y%m%d_%H%M' format.
    For a filename /my/path/myexcel.xlsx the function would return /my/path/myexcel_20170101_1305.xlsx.
    If the file already exists the function will add seconds to the date to attempt to get a unique name.

    :param filename: string with fullpath to file or just the filename
    :param kwargs: dictionary. date_position: suffix or preffix, extension: string to replace extension
    :return: string with full path string incluiding the date and time
    """
    current_datetime = timezone.localtime(timezone.now()).strftime('%Y%m%d_%H%M%S')
    new_filename_data = dict()
    suffix_template = '{path}{separator}{filename_with_out_extension}_{datetime}.{extension}'
    prefix_template = '{path}{separator}{datetime}_{filename_with_out_extension}.{extension}'
    if '/' in filename and '\\' in filename:
        raise ValueError('Filename %s contains both / and \\ separators' % filename)
    if '\\' in filename:
        path_parts = filename.split('\\')
        file = path_parts[-1]
        path = '\\'.join(path_parts[:-1])
        separator = '\\'
    elif '/' in filename:
        path_parts = filename.split('/')
        file = path_parts[-1]
        path = '/'.join(path_parts[:-1])
        separator = '/'
    else:
        file = filename
        path = ''
        separator = ''

    new_filename_data['path'] = path
    parts = file.split('.')
    if kwargs.get('extension', None) is not None:
        new_filename_data['extension'] = kwargs['extension']
    else:
        new_filename_data['extension'] = parts[-1]

    new_filename_data['separator'] = separator
    new_filename_data['filename_with_out_extension'] = '.'.join(parts[:-1])
    new_filename_data['datetime'] = current_datetime[:-2]
    date_position = kwargs.get('date_position', 'suffix')
    if date_position == 'suffix':
        new_filename = suffix_template.format(**new_filename_data)
        if os.path.exists(new_filename):
            new_filename_data['datetime'] = current_datetime
            new_filename = suffix_template.format(**new_filename_data)
    else:
        new_filename = prefix_template.format(**new_filename_data)
        if os.path.exists(new_filename):
            new_filename_data['datetime'] = current_datetime
            new_filename = prefix_template.format(**new_filename_data)

    return new_filename
