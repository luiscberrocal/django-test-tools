import functools
import warnings

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
