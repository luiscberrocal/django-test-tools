from django.db import models
try:
    from django.utils.translation import ugettext_lazy as _
except:
    from django.utils.translation import gettext_lazy as _

# Create your models here.
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField


class Human(models.Model):
    MALE_SEX = 'M'
    FEMALE_SEX = 'F'
    SEX_CHOICES = ((MALE_SEX, _('Male')),
                   (FEMALE_SEX, _('Female')))

    NATIONAL_ID = 'NATIONAL_ID'
    DRIVERS_LICENSE = 'DRIVERS_LICENSE'
    PASSPORT = 'PASSPORT'
    OTHER = 'OTHER'

    NATIONAL_ID_TYPE_CHOICES = (
        (1, _('National Id')),
        (2, _('Drivers License')),
        (3, _('Passport')),
        (4, _('Other')),

    )

    first_name = models.CharField(_('First name'), max_length=60, null=True, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=60, null=True, blank=True)
    last_name = models.CharField(_('Last name'), max_length=60, null=True, blank=True)
    sex = models.CharField(_('Gender'), max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    national_id = models.CharField('National id', max_length=50)
    national_id_type = models.IntegerField(_('National id type'),
                                           choices=NATIONAL_ID_TYPE_CHOICES, default=NATIONAL_ID)
    country_for_id = CountryField(_('Country for id'))
    picture = models.ImageField(_('Picture'), null=True, blank=True)
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    blood_type = models.CharField('Blood type', max_length=4, null=True, blank=True)
    religion = models.CharField(_('Religion'), max_length=60, null=True, blank=True)

    class Meta:
        abstract = True


class Person(Human):
    document = models.FileField()
    salary = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    cell_phone = models.CharField(max_length=16, null=True)
