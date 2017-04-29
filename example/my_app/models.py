from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=20)

