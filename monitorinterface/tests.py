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
        host_ip3 = '10.10.10.12'
        
        Host.objects.create(ip=host_ip1).save()
        Host.objects.create(ip=host_ip2).save()
        Host.objects.create(ip=host_ip3).save()
        
        Metric.objects.create(host=Host.objects.get(ip=host_ip1), type='Type1', period_seconds=5).save()
        Metric.objects.create(host=Host.objects.get(ip=host_ip1), type='Type2', period_seconds=10).save()

        Metric.objects.create(host=Host.objects.get(ip=host_ip2), type='Type1', period_seconds=1).save()


    def test_MetricList_get(self):
 #       print("I am in 1st test")
        response = self.client.get(reverse('hosts_list'),format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"id":1,"ip":"10.10.10.10"},{"id":2,"ip":"10.10.10.11"},{"id":3,"ip":"10.10.10.12"}]
        )

    def test_MeasurementList_get(self):
#        print("I am in 2nd test")

        response = self.client.get(reverse('metric_list', kwargs={'host_id': 1}),format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"id":1,"type":"Type1","period_seconds":5},{"id":2,"type":"Type2","period_seconds":10}]
        )

        response = self.client.get(reverse('metric_list', kwargs={'host_id': 2}),format='json')
        self.assertEqual(response.status_code, 200) 
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"id":3,"type":"Type1","period_seconds":1}]
        )

        response = self.client.get(reverse('metric_list', kwargs={'host_id': 3}),format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            []
        )
    
    def test_MetricList_post(self):
#        print("I am in 3rd test")
        response = self.client.post(reverse('hosts_list'),{'ip':'10.10.10.10'},format='json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"id":4,"ip":"10.10.10.10"}
        )

        response = self.client.post(reverse('hosts_list'),{'ip':'10.10.10.10', 'ip':'10.10.10.11'},format='json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"id":4,"ip":"10.10.10.10", "id":5,"ip":"10.10.10.11"}
        )

        response = self.client.post(reverse('hosts_list'),format='json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"ip":["This field is required."]}
        )
        
    
    def test_MeasurementList_get(self):
#        print("I am in 4th test")
        response = self.client.post(reverse('metric_list', kwargs={'host_id': 1}), {'type':'Type1'},format='json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"id":4,"type":"Type1","period_seconds":0}
        )
        
        response = self.client.post(reverse('metric_list', kwargs={'host_id': 2}), {'type':'Type1', 'type':'Type2'},format='json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"id":5,"type":"Type2","period_seconds":0}
        )
        
        response = self.client.post(reverse('metric_list', kwargs={'host_id': 3}),format='json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'type': ['This field is required.']}
        )

        response = self.client.post(reverse('metric_list', kwargs={'host_id': 3}),{'type':'UnknownType'},format='json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"id":6,"type":"UnknownType","period_seconds":0}
        )