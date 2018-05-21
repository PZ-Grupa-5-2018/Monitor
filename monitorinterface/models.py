from django.db import models

CUSTOM_TYPES=['mean']
class Host(models.Model):
    ip = models.CharField(max_length=15)
    mac = models.CharField(max_length=17)
    name = models.CharField(max_length=1000,unique=True)
    cpu = models.CharField(max_length=1000)
    memory = models.CharField(max_length=1000)
    platform = models.CharField(max_length=1000)


class Metric(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="host")
    type = models.CharField(max_length=30)
    period_seconds = models.IntegerField()
    metric_id = models.IntegerField(default=0)

    @property
    def is_custom(self):
        return self.type in CUSTOM_TYPES


class Measurement(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name="metric")
    value = models.FloatField()
    timestamp = models.DateTimeField()
