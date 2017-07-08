import hashlib
import json
import os

from datetime import date, datetime
from django.utils import timezone
from .utils import create_output_filename_with_date

BLOCKSIZE = 65536


def hash_file(filename, algorithm='sha1', block_size=BLOCKSIZE):
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
    :param extension: extention of the filename
    :param delete_on_exit: If True the filename will be deleted.
    :return: the function
    """
    filename = create_output_filename_with_date('{}.{}'.format(func.__name__, extension))

    def function_t_return(*args):
        results = func(*args)
        if os.path.exists(filename) and delete_on_exit:
            os.remove(filename)
        return results
    function_t_return.filename = filename
    return function_t_return


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code
    taken from: https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
    """

    if isinstance(obj, (datetime, date)):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type %s not serializable" % type(obj))

def serialize_data(data, output_file=None, format='json',**kwargs):
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
    assert format in ['json'], 'Unsupported format {}'.format(format)
    if output_file is None:
        filename = create_output_filename_with_date('{}.{}'.format('serialize_data_q', format))
    elif os.path.isdir(output_file):
        filename = os.path.join(output_file,'{}.{}'.format('serialize_data_f', format))
    else:
        filename = output_file
    if format == 'json':
        with open(filename, 'w', encoding=kwargs.get('encoding', 'utf-8')) as fp:
            json.dump(data, fp, indent=kwargs.get('indent', 4),
                      default=json_serial, sort_keys=True)
    return filename


def add_date(filename, **kwargs):
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
        file=filename
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
    if date_position=='suffix':
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
