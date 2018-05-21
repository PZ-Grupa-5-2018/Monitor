from monitorinterface.models import Host, Metric, Measurement, CUSTOM_TYPES
from monitorinterface.serializers import HostSerializer, MetricSerializer, MeasurementSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import math
from django.utils import timezone


class HostList(generics.ListCreateAPIView):
    serializer_class = HostSerializer

    def get_queryset(self):
        self.queryset = Host.objects.all()
        self.filter_by_query_param('name')
        self.filter_by_query_param('ip')
        self.filter_by_query_param('cpu')
        self.filter_by_query_param('memory')
        query = self.request.query_params.get("active", None)
        if query is not None and query in ['true', 't', 'True']:
            created_time = timezone.now() - timezone.timedelta(minutes=1)
            metric_ids = set((o.metric.id for o in Measurement.objects.filter(timestamp__gt=created_time)))
            host_ids = set((o.host.id for o in Metric.objects.filter(id__in=metric_ids)))
            self.queryset = self.queryset.filter(id__in=host_ids)
        return self.queryset

    def filter_by_query_param(self, query_param):
        query = self.request.query_params.get(query_param, None)
        if query is not None:
            filter_dict = {query_param + "__icontains": query}
            self.queryset = self.queryset.filter(**filter_dict)

    def post(self, request, format=None):
        serializer = HostSerializer(data=request.data)
        if serializer.is_valid():
            duplicates = Host.objects.filter(name=serializer.validated_data["name"]).filter(
                mac=serializer.validated_data["mac"])
            if not duplicates:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(HostSerializer(duplicates[0]).data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MultiFilterDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_fields = []

    def extend_filter(self, filter):
        return (filter)

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if field in self.kwargs:
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **self.extend_filter(filter))  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class HostDetail(MultiFilterDetail):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    lookup_fields = ['pk', 'name']


class MetricList(generics.ListCreateAPIView):
    serializer_class = MetricSerializer

    def get_queryset(self):
        if "host_id" in self.kwargs:
            queryset = Metric.objects.filter(host__id=self.kwargs['host_id'])
        else:
            queryset = Metric.objects.filter(host__name=self.kwargs['host_name'])
        value = self.request.query_params.get("is_custom", None)
        if value is not None:
            if value in ['true', 't', 'True']:
                queryset = queryset.filter(type__in=CUSTOM_TYPES)
            else:
                queryset = queryset.exclude(type__in=CUSTOM_TYPES)
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = MetricSerializer(data=request.data)
        if serializer.is_valid():
            if "host_id" in kwargs:
                duplicates = Metric.objects.filter(type=serializer.validated_data["type"]).filter(
                    host__id=kwargs["host_id"])
            else:
                duplicates = Metric.objects.filter(type=serializer.validated_data["type"]).filter(
                    host__name=kwargs["host_name"])
            if not duplicates:
                if "host_id" in kwargs:
                    serializer.validated_data["host_id"] = kwargs["host_id"]
                else:
                    serializer.validated_data["host_id"] = get_object_or_404(Host, name=kwargs["host_name"]).id
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(MetricSerializer(duplicates[0]).data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MetricDetail(MultiFilterDetail):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    lookup_fields = ['pk', 'type', 'host_id']

    def extend_filter(self, filter):
        ret = filter
        if "host_name" in self.kwargs:
            ret['host_id'] = get_object_or_404(Host, name=self.kwargs["host_name"]).id
        return ret


class MeasurementList(APIView):
    def get_metric_id(self):
        if "host_name" in self.kwargs:
            host_id = get_object_or_404(Host, name=self.kwargs["host_name"]).id
        else:
            host_id = self.kwargs["host_id"]
        if "metric_name" in self.kwargs:
            return get_object_or_404(Metric, type=self.kwargs["metric_name"], host_id=host_id).id
        else:
            return self.kwargs["metric_id"]

    def get(self, request, *args, **kwargs):
        metric_id = self.get_metric_id()
        metric = get_object_or_404(Metric, pk=metric_id)
        if metric.is_custom:
            parent_metric = get_object_or_404(Metric, pk=metric.metric_id)
            measurements = Measurement.objects.filter(metric__id=metric.metric_id).order_by('-timestamp')
            ms = []
            measurement_count = math.ceil(metric.period_seconds / parent_metric.period_seconds)
            for index in range(len(measurements) - measurement_count + 1):
                value = sum(m.value for m in measurements[index:index + measurement_count]) / measurement_count
                ms.append(Measurement(value=value, timestamp=measurements[index].timestamp, id=index))

        else:
            ms = Measurement.objects.filter(metric__id=metric_id)
            since = self.request.query_params.get('since', None)
            if since is not None:
                ms = ms.filter(timestamp__gt=since)
        count = self.request.query_params.get('count', None)
        if count is None:
            count = 10
        count = int(count)
        ms = ms[:count]
        serializer = MeasurementSerializer(ms, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        metric_id = self.get_metric_id()
        serializer = MeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["metric_id"] = metric_id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
