import contextlib
import subprocess

import pip
import pkg_resources

from django_test_tools.utils import versiontuple

if versiontuple(pip.__version__) >= (10, 0, 0):
    from pip._internal.req import parse_requirements
    from pip._internal.req.req_install import InstallRequirement
else:
    from pip.req import parse_requirements, InstallRequirement

import re

import requests
import logging

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def capture():
    import sys
    from io import StringIO
    oldout, olderr = sys.stdout, sys.stderr
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


def parse_pip_list(line):
    regexp = re.compile(r'([\w\-]*)\s\(([\w\-_\.]*)\)\s\-\sLatest:\s([\w\-_\.]*)\s\[([a-z]*)\]')
    regexp_list = re.compile(r'([\w\-]*)\s+([\w\-_\.]*)')
    match = regexp.match(line)
    if match:
        library = dict()
        library['name'] = match.group(1).lower()
        library['current_version'] = match.group(2)
        library['new_version'] = match.group(3)
        return library
    match_list = regexp_list.match(line)
    if match_list:
        library = dict()
        library['name'] = match_list.group(1).lower()
        library['current_version'] = match_list.group(2)
        return library

    return None


def get_latest_version(package_name):
    url = 'https://pypi.python.org/pypi/{}/json'.format(package_name)
    r = requests.get(url)
    versions = sorted(r.json()["releases"], key=pkg_resources.parse_version)
    return versions[-1]


def parse_comes_from(comes_from):
    regexp = re.compile(r'(\-r)\s([/\w\.\-]*)\s\(line\s(\d*)\)')
    match = regexp.match(comes_from)
    if match:
        return match.group(1), match.group(2), int(match.group(3))
    else:
        raise ValueError('Invalid comes from "{}"'.format(comes_from))


def parse_specifier(specifier):
    regexp = re.compile(r'((?:[=>])=)([\w\-_\.]*)')
    match = regexp.match(specifier)
    if match:
        return match.group(1), match.group(2)
    else:
        raise ValueError('Invalid speficier "{}"'.format(specifier))


def read_requirement_file(req_file):
    # print('pip version {}'.format(pip.__version__))
    requirements = dict()
    for item in parse_requirements(req_file, session="somesession"):
        if isinstance(item, InstallRequirement):
            requirement = dict()
            requirement['name'] = item.name
            if len(str(item.req.specifier)) > 0:
                operator, version = parse_specifier(str(item.req.specifier))
                requirement['operator'] = operator
                requirement['version'] = version
            requirement['comes_from'] = dict()
            requirement['comes_from']['value'] = item.comes_from
            file_indicator, filename, line_no = parse_comes_from(item.comes_from)
            requirement['comes_from']['file_indicator'] = file_indicator
            requirement['comes_from']['filename'] = filename
            requirement['comes_from']['line_no'] = line_no

            requirements[item.name] = requirement
    return requirements


def list_outdated_libraries():
    return list_libraries(True)


def list_libraries(outdated=False):
    command_list = ['pip', 'list']
    if outdated:
        command_list.append('--outdated')
    pip_list = subprocess.check_output(command_list)
    # pip.main(['list', '--outdated'])
    library_lines = pip_list.decode("utf-8").split('\n')
    outdated_libraries = list()
    for line in library_lines:
        library = parse_pip_list(line)
        if library is not None:
            outdated_libraries.append(library)
    return outdated_libraries


def update_outdated_libraries(requirement_file, **kwargs):
    """
    Updates the requirements to their latest version.

    :param requirement_file: String with the path to the requirement fiel
    :param kwargs:
    :return: list of dictionaries containting the changes
    """
    requirements = read_requirement_file(requirement_file)
    outdated_libraries = list_outdated_libraries()
    changes = list()
    for outdated_library in outdated_libraries:
        library_name = outdated_library['name']
        if requirements.get(library_name):
            change = dict()
            change['library_name'] = library_name
            change['filename'] = requirements[library_name]['comes_from']['filename']
            line_no = requirements[library_name]['comes_from']['line_no'] - 1
            operator = requirements[library_name]['operator']
            with open(change['filename'], 'r') as file:
                data = file.readlines()
            new_value = '{}{}{}\n'.format(library_name, operator, outdated_library['new_version'])
            change['previous'] = data[line_no].strip('\n')
            change['new'] = new_value.strip('\n')
            data[line_no] = new_value
            with open(change['filename'], 'w') as file:
                file.writelines(data)
            change['line_no'] = line_no
            changes.append(change)
    return changes
