import string

from random import randint
from pytz import timezone

from django.conf import settings

from factory import Iterator
from factory import LazyAttribute
from factory import SubFactory
from factory import lazy_field
from factory.django import DjangoModelFactory, FileField
from factory.fuzzy import FuzzyText, FuzzyInteger
from faker import Factory as FakerFactory

faker = FakerFactory.create()


class PersonFactory(DjangoModelFactory):

    class Meta:
        model = Person
        
    
    first_name = LazyAttribute(lambda x: faker.text(max_nb_chars=60))
    middle_name = LazyAttribute(lambda x: FuzzyText(length=60, chars=string.digits).fuzz())
    last_name = LazyAttribute(lambda x: faker.text(max_nb_chars=60))
    sex = Iterator((('M', 'Male'), ('F', 'Female')), getter=lambda x: x[0])
    national_id = LazyAttribute(lambda x: FuzzyText(length=50, chars=string.digits).fuzz())
    national_id_type = LazyAttribute(lambda o: randint(3, 3))
    country_for_id = Iterator(['PA', 'US', 'GB',])
    # Field type ImageField for field picture is not currently supported
    date_of_birth = LazyAttribute(lambda x: faker.date_between(start_date="-1y", end_date="today", tzinfo=timezone(settings.TIME_ZONE)))
    blood_type = LazyAttribute(lambda x: FuzzyText(length=4, chars=string.ascii_letters).fuzz())
    religion = LazyAttribute(lambda x: faker.text(max_nb_chars=60))
    document = FileField(filename='document.txt')
    # Field type CurrencyField for field salary_currency is not currently supported
    salary = LazyAttribute(lambda x: faker.pydecimal(left_digits=12, right_digits=2, positive=True))
    cell_phone = LazyAttribute(lambda x: faker.text(max_nb_chars=16))
    # Field type EmailField for field email is not currently supported
    # Field type JSONField for field metadata is not currently supported
