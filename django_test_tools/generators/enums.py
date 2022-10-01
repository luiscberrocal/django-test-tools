from enum import Enum


class SupportedFields(str, Enum):
    BooleanField
    CharFiele
    CountryField
    DateField
    DateTimeField
    DecimalField
    ForeignKey
    GenericIPAddressField
    IntegerField
    MoneyField
    TextField