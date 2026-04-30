from django.db import models

# Create your models here.
class Site(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    workers_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name