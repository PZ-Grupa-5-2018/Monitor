from django.db import models


# Create your models here.
class Measurement(models.Model):
    mac_address = models.CharField(max_length=24)
    ip_address = models.CharField(max_length=16)
    memory_usage = models.DecimalField(decimal_places=2, max_digits=10)
    memory_total = models.DecimalField(decimal_places=2, max_digits=10)
    cpu_usage = models.DecimalField(decimal_places=2, max_digits=10)
    disk_usage = models.DecimalField(decimal_places=2, max_digits=10)
    disk_total = models.DecimalField(decimal_places=2, max_digits=10)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.mac_address)
