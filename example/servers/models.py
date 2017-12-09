from django.db import models


class OperatingSystem(models.Model):
    name = models.CharField(max_length=20)
    version = models.CharField(max_length=5)
    licenses_available = models.IntegerField()
    cost = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        unique_together = ('name', 'version')


class Server(models.Model):
    PRODUCTION = 'PROD'
    DEVELOPMENT = 'DEV'
    USE_CHOICES = ((PRODUCTION, 'Prod'),
                   (DEVELOPMENT, 'Dev'))
    name = models.CharField(max_length=20, unique=True)
    notes = models.TextField()
    virtual = models.BooleanField()
    ip_address = models.GenericIPAddressField()
    created = models.DateTimeField()
    online_date = models.DateField()
    operating_system = models.ForeignKey(OperatingSystem, related_name='servers', on_delete=models.CASCADE)
    server_id = models.CharField(max_length=6)
    use = models.CharField(max_length=4, choices=USE_CHOICES, default=DEVELOPMENT)
    comments = models.TextField(null=True, blank=True)


