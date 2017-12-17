import hashlib
import json
import os
import pickle
import shutil
from datetime import date, datetime

from django.conf import settings
from django.utils import timezone

BLOCKSIZE = 65536


def create_dated(filename):
    """
    Based on the filename will create a full path filename including the date and time in '%Y%m%d_%H%M' format.
    The path to the filename will be set in the TEST_OUTPUT_PATH settings variable.

    If the TEST_OUTPUT_PATH folder doesn't exist the function will create it.

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


def hash_file(filename, algorithm='sha1', block_size=BLOCKSIZE):
    """
    Creates a unique hash for a file.
    :param filename: String with the full path to the file
    :param algorithm: String Algorithm to create the hash
    :param block_size: int for the size of the block while reading the file
    :return: string the hash for the file
    """
    try:
        hasher = getattr(hashlib, algorithm)()
    except AttributeError:
        raise ValueError('{} is not a valid hashing algorithm'.format(algorithm))

    with open(filename, 'rb') as afile:
        buf = afile.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(block_size)
    return hasher.hexdigest()


def parametrized(dec):
    """
    Need to study this code.
    Got it from http://stackoverflow.com/questions/5929107/python-decorators-with-parameters
    :param dec:
    :return:
    """

    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parametrized
def temporary_file(func, extension, delete_on_exit=True):
    """
    This method decorator creates a filename with date using the provided extension and delete the file after the method
    has been executed.

    The settings.TEST_OUTPUT_PATH must be configured in your settings file.

    .. code-block:: python

        @temporary_file('json')
        def test_temporary_file_decorator(self):
            filename = self.test_temporary_file_decorator.filename
            ... write to the file ...


    :param func: function to decorate
    :param extension: extension of the filename without the dot
    :param delete_on_exit: If True the filename will be deleted.
    :return: the function
    """
    filename = create_dated('{}.{}'.format(func.__name__, extension))

    def function_t_return(*args):
        results = func(*args)
        if os.path.exists(filename) and delete_on_exit:
            os.remove(filename)
        return results

    function_t_return.filename = filename
    return function_t_return


def shorten_path(path, level=2, current_level=1):
    """
    This method shortens the path by eliminating the folders on top.

    .. code-block:: python

        filename = '/user/documents/personal/file.txt'
        shortened = shorten_path(filename)
        self.assertEqual(shortened, 'personal/file.txt')


    :param path: string full path for the filename
    :param level: int, number of levels to show.
    :param current_level: int, recursing level.
    :return: string shortened path
    """
    if level == 0:
        raise ValueError('The minimum level accepted is one')
    path, tail = os.path.split(path)
    if level == current_level:
        return tail
    else:
        if path != os.path.sep:
            return shorten_path(path, level, current_level + 1) + os.path.sep + tail
        return tail


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code
    taken from: https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
    """

    if isinstance(obj, (datetime, date)):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type %s not serializable" % type(obj))


def serialize_data(data, output_file=None, format='json', **kwargs):
    """
    Quick function to serialize a data to file. The data keys will be saved in an alphabetical order
    for consistency purposes.
    If no output_file is supplied the function will created a dated file in the settings.TEST_OUTPUT_PATH folder.
    if the output_file is a folder the dated file will be created on the supplied folder with the serialized date.
    if the output_file is a file the data will be serialized to thar file

    :param data: Dictionary or list to serialize
    :param format: Format to serialize to. Currently json is the only one supported
    :param output_file: File to output the data to
    :param kwargs:
    """
    assert format in ['json', 'pickle'], 'Unsupported format {}'.format(format)
    base_filename = kwargs.get('base_filename', 'serialized_data')

    if output_file is None:
        filename = create_dated('{}.{}'.format(base_filename, format))
    elif os.path.isdir(output_file):
        filename = os.path.join(output_file, '{}.{}'.format(base_filename, format))
    else:
        filename = output_file
    if format == 'json':
        with open(filename, 'w', encoding=kwargs.get('encoding', 'utf-8'), newline='\n') as fp:
            json.dump(data, fp, indent=kwargs.get('indent', 4),
                      default=json_serial, sort_keys=True)
    elif format == 'pickle':
        with open(filename, 'wb') as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

    return filename


def add_date(filename, **kwargs):
    """
    Adds to a filename the current date and time in '%Y%m%d_%H%M' format.
    For a filename /my/path/myexcel.xlsx the function would return /my/path/myexcel_20170101_1305.xlsx.
    If the file already exists the function will add seconds to the date to attempt to get a unique name.

    The function will detect if another file exists with the same name if it exist it will append seconds to the
    filename. For example if file /my/path/myexcel_20170101_1305.xlsx alread exist thte function will return
    /my/path/myexcel_20170101_130521.xlsx.

    :param filename: string with fullpath to file or just the filename
    :param kwargs: dictionary. date_position: suffix or preffix, extension: string to replace extension
    :return: string with full path string including the date and time
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
        if len(parts) > 1:
            new_filename_data['extension'] = parts[-1]
        else:
            new_filename_data['extension'] = ''

    new_filename_data['separator'] = separator
    if new_filename_data['extension'] == '':
        new_filename_data['filename_with_out_extension'] = parts[0]
    else:
        new_filename_data['filename_with_out_extension'] = '.'.join(parts[:-1])
    new_filename_data['datetime'] = current_datetime[:-2]  # Seconds are stripped

    date_position = kwargs.get('date_position', 'suffix')
    if date_position == 'suffix':
        new_filename = suffix_template.format(**new_filename_data)
        if os.path.exists(new_filename):
            new_filename_data['datetime'] = current_datetime
            new_filename = suffix_template.format(**new_filename_data)
        if new_filename_data['extension'] == '':
            new_filename = new_filename[:-1]
    else:
        new_filename = prefix_template.format(**new_filename_data)
        if os.path.exists(new_filename):
            new_filename_data['datetime'] = current_datetime
            new_filename = prefix_template.format(**new_filename_data)
        if new_filename_data['extension'] == '':
            new_filename = new_filename[:-1]

    return new_filename


class TemporaryFolder:
    def __init__(self, base_name, delete_on_exit=True):
        self.new_path = create_dated(base_name)
        self.delete_on_exit = delete_on_exit

    def __enter__(self):
        os.mkdir(self.new_path)
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.saved_path)
        if self.delete_on_exit:
            shutil.rmtree(self.new_path)

    def write(self, filename, content):
        with open(filename, 'w', encoding='utf-8') as file:
            if isinstance(content, str):
                file.writelines(content)
            elif isinstance(content, list):
                for line in content:
                    file.write(line)
                    file.write('\n')
            else:
                file.writelines(str(content))
        return os.path.join(self.new_path, filename)
