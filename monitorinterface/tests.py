from django.test import TestCase

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import reverse
from monitorinterface.models import Host, Metric, Measurement
from monitorinterface.serializers import HostSerializer, MetricSerializer, MeasurementSerializer
from monitorinterface.views import MeasurementList, MetricList

class MetricListTest(TestCase):
    ''' Test module for MetricList model '''

    def setUp(self):
        host_ip1 = '10.10.10.10'
        host_ip2 = '10.10.10.11'
        Host.objects.create(ip=host_ip1).save()
        Host.objects.create(ip=host_ip2).save()

    def test_MetricList_get(self):
        response = self.client.get(reverse('hosts_list'),format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"id":1,"ip":"10.10.10.10"},{"id":2,"ip":"10.10.10.11"}]
        )



# Create your tests here.
