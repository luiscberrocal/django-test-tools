import csv
import re


class Flake8Parser(object):
    """
    3     E124 closing bracket does not match visual indentation
    6     E127 continuation line over-indented for visual indent
    11    E128 continuation line under-indented for visual indent
    2     E221 multiple spaces before operator
    1     E222 multiple spaces after operator
    10    E225 missing whitespace around operator
    6     E231 missing whitespace after ','
    2     E251 unexpected spaces around keyword / parameter equals
    4     E261 at least two spaces before inline comment
    4     E262 inline comment should start with '# '
    8     E265 block comment should start with '# '
    4     E266 too many leading '#' for block comment
    2     E271 multiple spaces after keyword
    5     E302 expected 2 blank lines, found 1
    7     E303 too many blank lines (3)
    2     E402 module level import not at top of file
    8     E501 line too long (123 > 120 characters)
    17    F401 'django.contrib.admin' imported but unused
    25    F405 'env' may be undefined, or defined from star imports: .base
    1     F811 redefinition of unused 'RemarksManager' from line 3
    7     F841 local variable 'response' is assigned to but never used
    2     W293 blank line contains whitespace
    6     W391 blank line at end of file
    """

    def __init__(self):
        self.summary_regexp = re.compile(r'(\d+)\s+((?:W|E|F)\d+)\s([\w\s\'.#,()>:]*)')
        self.fieldnames = ['count', 'rule', 'description']

    def parse_summary(self, filename):
        pep8_findings = list()
        with open(filename, 'r', encoding='utf-8') as flake_file:
            for line in flake_file.readlines():
                match = self.summary_regexp.match(line.rstrip('\n'))
                if match:
                    data = dict()
                    data['count'] = match.group(1)
                    data['rule'] = match.group(2)
                    data['description'] = match.group(3)
                    pep8_findings.append(data)
        return pep8_findings

    def write_summary(self, source_filename, target_filename):
        pep8_findings = self.parse_summary(source_filename)
        with open(target_filename, 'w', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writeheader()
            for data in pep8_findings:
                csv_writer.writerow(data)


class RadonParser(object):
    """


    config/settings/test.py
        LOC: 61
        LLOC: 12
        SLOC: 23
        Comments: 23
        Single comments: 22
        Multi: 4
        Blank: 12
        - Comment Stats
            (C % L): 38%
            (C % S): 100%
            (C + M % L): 44%
    ** Total **
        LOC: 2149
        LLOC: 894
        SLOC: 1311
        Comments: 335
        Single comments: 310
        Multi: 128
        Blank: 400
        - Comment Stats
            (C % L): 16%
            (C % S): 26%
            (C + M % L): 22%
    """

    def __init__(self):
        self.totals_match_regexp = re.compile(r'\s*\*\*\sTotal\s\*\*')
        self.results_regexp = re.compile(r'^\s+(LOC|LLOC|SLOC|Comments|Single\scomments|Multi|Blank):\s(\d+)')
        self.fieldnames = ['loc', 'lloc', 'sloc', 'comments', 'single_comments', 'multi', 'blank']

    def parse_totals(self, filename):
        data = dict()
        totals_found = False
        with open(filename, 'r', encoding='utf-8') as flake_file:
            for line in flake_file.readlines():
                match = self.totals_match_regexp.match(line.rstrip('\n'))
                if match:
                    totals_found = True
                if totals_found:
                    data_match = self.results_regexp.match(line.rstrip('\n'))
                    if data_match:
                        key = data_match.group(1).lower().replace(' ', '_')
                        data[key] = int(data_match.group(2))
        return data

    def write_totals(self, source_filename, target_filename):
        radon_findings = self.parse_totals(source_filename)
        with open(target_filename, 'w', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writeheader()
            csv_writer.writerow(radon_findings)
