import functools
import json
import os
import re
import time
import warnings
from datetime import datetime, date, timedelta

import pytz
from django.conf import settings
from django.utils import timezone
from openpyxl.compat import deprecated

from .file_utils import add_date

__author__ = 'lberrocal'


def versiontuple(v):
    return tuple(map(int, (v.split("."))))

def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def convert_to_snake_case(camel_case):
    """
    Converts a CamelCase name to snake case.
    ..code-block:: python

        camel_case = 'OperatingSystemLongName'
        snake_case = convert_to_snake_case(camel_case)
        self.assertEqual(snake_case, 'operating_system_long_name')

    :param camel_case: string. Camel case name
    :return: string. Snake case name
    """
    s1 = first_cap_re.sub(r'\1_\2', camel_case)
    return all_cap_re.sub(r'\1_\2', s1).lower()


@deprecated('Should use django_test_tools.file_utils.create_dated() function')
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


@deprecated('Should use django_test_tools.file_utils.add_date() function')
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


def weekdays(start_date, end_date):
    """
    Returns a generator with the dates of the week days between the start and end date

    .. code-block:: python

        start_date = datetime.date(2016, 10, 3)  # Monday
        end_date = datetime.date(2016, 10, 7)  # Friday
        days = list(weekdays(start_date, end_date))
        self.assertEqual(5, len(days))

    :param start_date: date. Start date
    :param end_date: date. End date
    """
    weekend = set([5, 6])
    for n in range(int((end_date - start_date).days) + 1):
        dt = start_date + timedelta(n)
        if dt.weekday() not in weekend:
            yield dt
        else:
            continue


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def force_date_to_datetime(unconverted_date, tzinfo=pytz.UTC):
    converted_datetime = date(year=unconverted_date.year,
                              month=unconverted_date.month,
                              day=unconverted_date.day,
                              hour=0,
                              minute=0,
                              second=0,
                              tzinfo=tzinfo)
    return converted_datetime


class Timer:
    """
    Class to measure time elapsed

    Example:

    .. code:: python

            def test_performance(self):
                with Timer() as stopwatch:
                    web_service = WebServiceUtil()
                    web_service.consume_date(12)
                elapsed_milliseconds = stopwatch.elapsed*1000
                logger.debug('Elapsed: {} ms'.format(elapsed_milliseconds))
                self.assertTrue(elapsed_milliseconds <= 500)

    """

    def __init__(self):
        self.elapsed = 0.0
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = time.perf_counter()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = time.perf_counter()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    def get_elapsed_time(self):
        hours, remainder = divmod(self.elapsed, 3600)
        mins, secs = divmod(remainder, 60)
        return int(hours), int(mins), secs

    def get_elapsed_time_str(self):
        return '%d h %d m %.2f s' % self.get_elapsed_time()

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


def load_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def datetime_to_local_time(date_time):
    """
    Converts a naive date to a time zoned date based in hte setting.TIME_ZONE variable. If the date has already a time zone
    it will localize the date.
    :param date_time: date or datetime to be localized
    :return: localized non naive datetime
    """
    if isinstance(date_time, date):
        date_time = datetime.combine(date_time, datetime.min.time())

    is_naive = date_time.tzinfo is None or date_time.tzinfo.utcoffset(date_time) is None
    time_zone = pytz.timezone(settings.TIME_ZONE)
    if is_naive:
        return time_zone.localize(date_time)
    else:
        return date_time.astimezone(time_zone)


class SpanishDate(object):
    def __init__(self):
        self.spanish_months = {'Ene': 'Jan', 'Feb': 'Feb', 'Mar': 'Mar', 'Abr': 'Apr', 'May': 'May',
                               'Jun': 'Jun', 'Jul': 'Jul', 'Ago': 'Aug', 'Sep': 'Sep', 'Oct': 'Oct',
                               'Nov': 'Nov', 'Dic': 'Dec'}
        self.english_months = dict()
        for k, v in self.spanish_months.items():
            self.english_months[v] = k

        self.date_format = '%d-%b-%y'
        self.datetime_format = '%d-%b-%y %H:%M'

        month_reg = '|'.join(self.spanish_months.values())
        regex = r'([0123][0-9])-(' + month_reg + ')-([\d]{2})$'
        self.date_reg_exp_en = re.compile(regex)

        regex = regex[:-1] + r' ([012][0-9]:[0-5][0-9])'
        self.datetime_reg_exp_en = re.compile(regex)

        month_reg = '|'.join(self.spanish_months.keys())
        regex = r'([0123][0-9])-(' + month_reg + ')-([\d]{2})$'
        self.date_reg_exp_es = re.compile(regex)

        regex = regex[:-1] + r' ([012][0-9]:[0-5][0-9])'
        self.datetime_reg_exp_es = re.compile(regex)

    def _get_date_parts(self, match, input_lang='es'):
        day = match.group(1)
        if input_lang == 'es':
            month = self.spanish_months[match.group(2)]
        else:
            month = self.english_months[match.group(2)]
        year = match.group(3)
        return day, month, year

    def parse(self, str_date):
        match = self.date_reg_exp_es.match(str_date)
        date_to_parse = None
        if match:
            day, month, year = self._get_date_parts(match)
            english_date = '{}-{}-{}'.format(day, month, year)
            date_to_parse = datetime_to_local_time(datetime.strptime(english_date, self.date_format)).date()
        else:
            match = self.datetime_reg_exp_es.match(str_date)
            if match:
                day, month, year = self._get_date_parts(match)
                time = match.group(4)
                english_date = '{}-{}-{} {}'.format(day, month, year, time)
                date_to_parse = datetime_to_local_time(datetime.strptime(english_date, self.datetime_format))
        return date_to_parse

    def to_string(self, m_date):

        if isinstance(m_date, datetime):
            str_date = m_date.strftime(self.datetime_format)
            match = self.datetime_reg_exp_en.match(str_date)
            if match:
                day, month, year = self._get_date_parts(match, 'en')
                time = match.group(4)
                return '{}-{}-{} {}'.format(day, month, year, time)
        elif isinstance(m_date, date):
            str_date = m_date.strftime(self.date_format)
            match = self.date_reg_exp_en.match(str_date)
            # date = None
            if match:
                day, month, year = self._get_date_parts(match, 'en')
                return '{}-{}-{}'.format(day, month, year)
        return None


spanish_date_util = SpanishDate()


def parse_spanish_date(str_date):
    return spanish_date_util.parse(str_date)
