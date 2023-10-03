from django.db import models
from django.utils import timezone

# Create your models here.


class SubnetPingInfo(models.Model):
    destination = models.CharField()
    type = models.CharField()
    status = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now())
