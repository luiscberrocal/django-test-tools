import contextlib

import pip
import re

@contextlib.contextmanager
def capture():
    import sys
    from io import StringIO
    oldout,olderr = sys.stdout, sys.stderr
    try:
        out=[StringIO(), StringIO()]
        sys.stdout,sys.stderr = out
        yield out
    finally:
        sys.stdout,sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()

def parse_comes_from(comes_from):
    regexp = re.compile(r'(\-r)\s([/\w\.\-]*)\s\(line\s(\d*)\)')
    match = regexp.match(comes_from)
    if match:
        return match.group(1), match.group(2), match.group(3)
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
    requirements = list()
    for item in pip.req.parse_requirements(req_file, session="somesession"):
        if isinstance(item, pip.req.InstallRequirement):
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

            requirements.append(requirement)
    return requirements
