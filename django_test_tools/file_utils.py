import hashlib
import os

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

