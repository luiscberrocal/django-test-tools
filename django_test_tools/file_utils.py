import hashlib
import os

from django_test_tools.utils import create_output_filename_with_date

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
    filename = create_output_filename_with_date('{}.{}'.format(func.__name__, extension))
    def function_t_return(*args):
        results = func(*args)
        if os.path.exists(filename) and delete_on_exit:
            os.remove(filename)
        return results
    function_t_return.filename = filename
    return function_t_return

