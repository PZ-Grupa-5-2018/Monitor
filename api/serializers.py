from rest_framework import serializers

from .models import Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Measurement
        fields = (
            'id', 'mac_address', 'ip_address', 'memory_usage', 'memory_total', 'cpu_usage', 'disk_usage', 'disk_total',
            'date_created')
        read_only_fields = ('date_created',)
