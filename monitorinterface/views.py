from monitorinterface.models import Host, Metric, Measurement
from monitorinterface.serializers import HostSerializer, MetricSerializer, MeasurementSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import math


class HostList(generics.ListCreateAPIView):
    serializer_class = HostSerializer

    def get_queryset(self):
        self.queryset = Host.objects.all()
        self.filter_by_query_param('name')
        self.filter_by_query_param('ip')
        self.filter_by_query_param('cpu')
        self.filter_by_query_param('memory')
        return self.queryset

    def filter_by_query_param(self, query_param):
        query = self.request.query_params.get(query_param, None)
        if query is not None:
            filter_dict={query_param+"__icontains": query}
            self.queryset = self.queryset.filter(**filter_dict)


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
        metric = get_object_or_404(Metric, pk=metric_id)
        if metric.is_custom:
            parent_metric = get_object_or_404(Metric, pk=metric.metric_id)
            measurements = Measurement.objects.filter(metric__id=metric.metric_id).order_by('-timestamp')
            ms = []
            measurement_count = math.ceil(metric.period_seconds / parent_metric.period_seconds)
            for index in range(len(measurements) - measurement_count + 1):
                value = sum(m.value for m in measurements[index:index + measurement_count]) / measurement_count
                ms.append(Measurement(value=value, timestamp=measurements[index].timestamp))
            serializer = MeasurementSerializer(ms, many=True)
            return Response(serializer.data)
        else:
            measurements = Measurement.objects.filter(metric__id=metric_id)
            serializer = MeasurementSerializer(measurements, many=True)
            return Response(serializer.data)

    def post(self, request, metric_id, format=None):
        serializer = MeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["metric_id"] = metric_id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
