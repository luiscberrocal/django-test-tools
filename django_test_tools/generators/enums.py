from enum import Enum


class FieldType(str, Enum):
    """Supported fields."""
    AUTO = 'AutoField'
    IMAGE = 'ImageField'
    FILE = 'FileField'
    BOOLEAN = 'BooleanField'
    CURRENCY = 'CurrencyField'
    CHAR = 'CharField'
    COUNTRY = 'CountryField'
    DATE = 'DateField'
    DATETIME = 'DateTimeField'
    DECIMAL = 'DecimalField'
    FOREIGN_KEY = 'ForeignKey'
    GENERIC_IP_ADDRESS = 'GenericIPAddressField'
    INTEGER = 'IntegerField'
    MONEY = 'MoneyField'
    TEXT = 'TextField'
    JSON = 'JSONField'
    EMAIL = 'EmailField'
