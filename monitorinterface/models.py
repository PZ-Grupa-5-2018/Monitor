from django.db import models


class Host(models.Model):
    ip = models.CharField(max_length=15)


class Metric(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="host")
    type = models.CharField(max_length=30)
    period_seconds = models.IntegerField(default=0)

    @property
    def is_custom(self):
        return self.type in ['mean']


class Measurement(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name="metric")
    value = models.FloatField()
    timestamp = models.DateTimeField()