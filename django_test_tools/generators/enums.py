from enum import Enum


class FieldType(str, Enum):
    """Supported fields."""
    BOOLEAN = 'BooleanField'
    CHAR = 'CharField'
    COUNTRY = 'CountryField'
    DATE = 'DateField'
    DATETIME = 'DateTimeField'
    DECIMAL = 'DecimalField'
    FOREIGNKEY = 'ForeignKey'
    GENERIC_IP_ADDRESS = 'GenericIPAddressField'
    INTEGER = 'IntegerField'
    MONEY = 'MoneyField'
    TEXT = 'TextField'
