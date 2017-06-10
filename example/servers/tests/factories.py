
import string

from random import randint
from pytz import timezone

from django.conf import settings

from factory import Iterator
from factory import LazyAttribute
from factory import SubFactory
from factory import lazy_attribute
from factory.django import DjangoModelFactory, FileField
from factory.fuzzy import FuzzyText, FuzzyInteger
from faker import Factory as FakerFactory

from example.servers.models import OperatingSystem, Server

faker = FakerFactory.create()


class OperatingSystemFactory(DjangoModelFactory):
    class Meta:
        model = OperatingSystem

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=20))
    version = LazyAttribute(lambda x: faker.text(max_nb_chars=5))
    licenses_available = LazyAttribute(lambda o: randint(1, 100))
    cost = LazyAttribute(lambda x: faker.pydecimal(left_digits=5, right_digits=2, positive=True))

class ServerFactory(DjangoModelFactory):
    class Meta:
        model = Server

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=20))
    notes = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    virtual = Iterator([True, False])
    ip_address = LazyAttribute(lambda o: faker.ipv4(network=False))
    created = LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", end_date="now",
                                                           tzinfo=timezone(settings.TIME_ZONE)))
    online_date = LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", end_date="now",
                                                           tzinfo=timezone(settings.TIME_ZONE)))
    operating_system = SubFactory(OperatingSystemFactory)
    server_id = LazyAttribute(lambda x: FuzzyText(length=6, chars=string.digits).fuzz())
    use = Iterator(Server.USE_CHOICES, getter=lambda x: x[0])
    comments = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
