import json
import os
import re
import time
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Dict, Any

import pytz
from django.conf import settings


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
    weekend = {5, 6}
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
    :param date_time: <date> or <datetime> to be localized
    :return: localized non naive datetime
    """
    if isinstance(date_time, date) and not isinstance(date_time, datetime):
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


def clean_dict(dictionary: Dict[str, Any], split_dates: bool = False, **kwargs) -> Dict[str, Any]:
    """Function to clean a model dictionary. It will change:
    1. elements that are None to blank string so it will be valid for POST data.
    2. elements that are date to string value in format %Y-%m-%d or the value supplied in kwargs['date_format']
    3. elements that are datetime to string value in format %Y-%m-%d %H:%M:%S or the value supplied
    in kwargs['datetime_format']
    4. elements that are Decimal to float
    Since the Django admin splits the dates int 2 inputs if split_dates is True and the name of the field is start_date
    the function will create a start_date_0 with the date and a start_date_1 with the time.
    :param dictionary:
    :param split_dates:
    :return: dictionary """

    keys = list(dictionary.keys())

    for key in keys:
        if dictionary[key] is None:
            dictionary[key] = ''
        if type(dictionary[key]) == datetime:
            date_format = kwargs.get('datetime_format', '%Y-%m-%d %H:%M:%S')
            if split_dates:
                date_value, time_value = dictionary[key].strftime(date_format).split(' ')
                dictionary[f'{key}_0'] = date_value
                dictionary[f'{key}_1'] = time_value
            else:
                dictionary[key] = dictionary[key].strftime(date_format)
        if type(dictionary[key]) == date:
            date_format = kwargs.get('date_format', '%Y-%m-%d')
            dictionary[key] = dictionary[key].strftime(date_format)
        if isinstance(dictionary[key], Decimal):
            dictionary[key] = float(str(dictionary[key]))

    return dictionary
