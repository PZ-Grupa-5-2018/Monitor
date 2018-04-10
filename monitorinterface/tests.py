from django.test import TestCase

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from monitorinterface.models import Host, Metric, Measurement
from monitorinterface.serializers import HostSerializer, MetricSerializer, MeasurementSerializer
from monitorinterface.views import MeasurementList, MetricList

class MetricListTest(TestCase):
	''' Test module for MetricList model '''
	
	def SetUp(self):
		host_ip1 = '10.10.10.10'
		host_ip2 = '10.10.10.11'
	
		
		Host.objects.create(ip=host_ip1)
		Host.objects.create(ip=host_ip2)
		
		Metric.objects.create(host=Host.objects.get(ip=host_ip1), type='Type1', period_seconds = 5)
		Metric.objects.create(host=Host.objects.get(ip=host_ip1), type='Type2', period_seconds = 5)
		Metric.objects.create(host=Host.objects.get(ip=host_ip2), type='Type1', period_seconds = 3)
		
		Measurement.objects.create(metric=Metric.objects.get(metric_id=1), value=1.0, timestamp='03-03-2018 01:01:01')
		Measurement.objects.create(metric=Metric.objects.get(metric_id=1), value=1.0, timestamp='03-03-2018 01:01:01')
		Measurement.objects.create(metric=Metric.objects.get(metric_id=2), value=3.0, timestamp='03-03-2018 01:01:01')
		Measurement.objects.create(metric=Metric.objects.get(metric_id=2), value=4.0, timestamp='03-03-2018 01:01:01')
		Measurement.objects.create(metric=Metric.objects.get(metric_id=3), value=1.1, timestamp='03-03-2018 01:01:01')
		Measurement.objects.create(metric=Metric.objects.get(metric_id=3), value=1.667, timestamp='03-03-2018 01:01:01')
		
	def test_MetricList_get(self):
		host_ip1 = '10.10.10.10'
		host_ip2 = '10.10.10.11'		
		request = 'request'
		host1_id = 1
		host2_id = 2
		metricList_1 = MetricList.get(request, host1_id).format='json'
		metricList_2 = MetricList.get(request, host2_id).format='json'
		
		self.assertEqual(metricList_1, "")
		self.assertEqual(metricList_2, "")

	def test_MeasurementList_get(self):
		
		host_ip1 = '10.10.10.10'
		host_ip2 = '10.10.10.11'
		request = 'request'
		metric1_id = Metric.objects.get(host=Host.objects.get(ip=host_ip1), type='Type1', period_seconds = 5).metric_id
		metric2_id = Metric.objects.get(host=Host.objects.get(ip=host_ip1), type='Type2', period_seconds = 5).metric_id
		metric3_id = Metric.objects.get(host=Host.objects.get(ip=host_ip2), type='Type1', period_seconds = 3).metric_id
		
		self.assertEqual(MeasurementList.get(request, metric1_id), "")
		self.assertEqua2(MeasurementList.get(request, metric3_id), "")
		self.assertEqua3(MeasurementList.get(request, metric1_id), "")





# Create your tests here.
