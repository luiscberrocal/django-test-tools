from enum import Enum


class FieldType(str, Enum):
    """Supported fields."""
    BOOLEAN_FIELD = 'BooleanField'
    CHAR_FIELD = 'CharField'
    COUNTRY_FIELD = 'CountryField'
    DATE_FIELD = 'DateField'
    DATETIME_FIELD = 'DateTimeField'
    DECIMAL_FIELD = 'DecimalField'
    FOREIGNKEY = 'ForeignKey'
    GENERIC_IP_ADDRESS_FIELD = 'GenericIPAddressField'
    INTEGER_FIELD = 'IntegerField'
    MONEY_FIELD = 'MoneyField'
    TEXT_FIELD = 'TextField'
