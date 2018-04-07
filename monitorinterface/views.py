from monitorinterface.models import Host, Metric, Measurement
from monitorinterface.serializers import HostSerializer, MetricSerializer, MeasurementSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


class HostList(generics.ListCreateAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class HostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class MetricList(APIView):

    def get(self, request, host_id, format=None):
        metrics = Metric.objects.filter(host__id=host_id)
        serializer = MetricSerializer(metrics, many=True)
        return Response(serializer.data)

    def post(self, request, host_id, format=None):
        serializer = MetricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["host_id"] = host_id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MetricDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer


class MeasurementList(APIView):

    def get(self, request, metric_id, format=None):
        measurements = Metric.objects.filter(metric__id=metric_id)
        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)

    def post(self, request, metric_id, format=None):
        serializer = MeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["metric_id"] = metric_id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

