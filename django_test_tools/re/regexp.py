import re

# Credit to https://gist.github.com/codehack/6350492822e52b7fa7fe
# Modified in https://regex101.com/r/p1lKGt/1
ISO8601_REGEXP = re.compile(
    r'^(?P<full>((?P<year>\d{4})([/-]?(?P<mon>(0[1-9])|(1[012]))([/-]?'
    r'(?P<mday>(0[1-9])|([12]\d)|(3[01])))?)?(?:T(?P<hour>([01][0-9])|(?:2[0123]))(\:?'
    r'(?P<min>[0-5][0-9])(\:?(?P<sec>[0-5][0-9]([\,\.]\d{1,10})?))?)'
    r'(Z|([\-+](?:([01][0-9])|(?:2[0123]))(\:?(?:[0-5][0-9]))?)))))$')
EMAIL_REGEXP = re.compile(
    r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'
)
SHA256_REGEXP = re.compile(r'^[a-fA-F0-9]{64}')


class CommonRegExp(object):
    """
    This class is a utility for commonly used regular expressions.

    .. code-block:: python

        str_data = '10:45'
        common_regexp = CommonRegExp()
        regular_expression, key = common_regexp.match_regexp(str_data)
        self.assertEqual(regular_expression, '([0-1][0-9]|2[0-4]):([0-5][0-9])')
        self.assertEqual(key, 'time_military')

    if the strict keyword is used the class will add ^ at the begining and a $ at the end if the already are not present.

    """

    def __init__(self, **kwargs):
        self.strict = kwargs.get('strict', False)
        self.regular_expressions = dict()
        self.regular_expressions['time_military'] = {
            'pattern': r'([0-1][0-9]|2[0-4]):([0-5][0-9])'
        }
        self.regular_expressions['integer'] = {
            'pattern': r'^(\d+)$'
        }
        self.regular_expressions['decimal'] = {
            'pattern': r'(\d+\.\d+)'
        }
        self.regular_expressions['url'] = {
            'pattern': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        }
        if kwargs.get('reg_exps'):
            self.regular_expressions.update(kwargs.get('reg_exps'))

        self.regular_expressions_compiled = dict()
        for key, reg_exp in self.regular_expressions.items():
            # self.regular_expressions_compiled[key] = re.compile(reg_exp['pattern'])
            self.regular_expressions_compiled[key] = self._compile_regular_expression(self.regular_expressions[key])

    def match_regexp(self, value):
        for key, regexp in self.regular_expressions_compiled.items():
            match = regexp.match(value)
            if match:
                return regexp.pattern, key

        return None, None

    def add_regular_expression(self, name, pattern, **kwargs):
        regexp_dict = dict()
        regexp_dict['pattern'] = pattern
        if kwargs.get('strict') is not None:
            regexp_dict['strict'] = kwargs.get('strict')
        self.regular_expressions_compiled[name] = self._compile_regular_expression(regexp_dict)

    def _compile_regular_expression(self, regexp_dict):
        if (self.strict or regexp_dict.get('strict')) and not regexp_dict['pattern'].startswith('^'):
            regexp_dict['pattern'] = '^{}'.format(regexp_dict['pattern'])

        if (self.strict or regexp_dict.get('strict')) and not regexp_dict['pattern'].endswith('$'):
            regexp_dict['pattern'] = '{}$'.format(regexp_dict['pattern'])
        return re.compile(regexp_dict['pattern'])
