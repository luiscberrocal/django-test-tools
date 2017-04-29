from django.db import models

class OperatingSystem(models.Model):
    name = models.CharField(max_length=20)
    version = models.CharField(max_length=3)
    licenses_available = models.IntegerField()
    cost = models.DecimalField(decimal_places=2, max_digits=7)


class Server(models.Model):
    name = models.CharField(max_length=20)
    notes = models.TextField()
    virtual = models.BooleanField()
    ip_address = models.GenericIPAddressField()
    created = models.DateTimeField()
    online_date = models.DateField()
    operating_system = models.ForeignKey(OperatingSystem)


