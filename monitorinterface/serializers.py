from rest_framework import serializers
from monitorinterface.models import Host, Metric, Measurement


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ('id', 'ip', 'mac', 'name', 'cpu', 'memory','platform')


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ('id', 'type', 'metric_id', 'period_seconds')


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('value', 'timestamp')
