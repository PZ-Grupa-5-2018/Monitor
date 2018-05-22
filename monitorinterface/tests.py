from django.test import TestCase
from django.shortcuts import reverse
from monitorinterface.models import Host, Metric, Measurement


class MetricListTest(TestCase):
    def setUp(self):
        host_ip1 = '10.10.10.10'
        host_ip2 = '10.10.10.11'
        host_ip3 = '10.10.10.12'
        Host.objects.create(cpu='Intel i3', ip=host_ip1, mac='00:0A:E6:3E:FD:E1', memory='32G', name='host1',platform="windows").save()
        Host.objects.create(cpu='Intel i5', ip=host_ip2, mac='00:1A:E6:3E:FD:E1', memory='16G', name='host2',platform="windows").save()
        Host.objects.create(cpu='Intel i7', ip=host_ip3, mac='00:2A:E6:3E:FD:E1', memory='8G', name='host3',platform="windows").save()

        Metric.objects.create(host=Host.objects.get(ip=host_ip1), type='Type1', period_seconds=5).save()
        Metric.objects.create(host=Host.objects.get(ip=host_ip1), type='mean', period_seconds=10).save()

        metric_for_custom = Metric.objects.create(host=Host.objects.get(ip=host_ip2), type='Type2', period_seconds=5)
        metric_for_custom.save()
        Metric.objects.create(host=Host.objects.get(ip=host_ip2), type='mean', period_seconds=1,
                              metric_id=metric_for_custom.id).save()

        Measurement.objects.create(metric=Metric.objects.get(id=1), value=1.0, timestamp='2018-04-11T18:52:17.863018Z')
        Measurement.objects.create(metric=Metric.objects.get(id=1), value=2.201,
                                   timestamp='2018-04-11T18:52:17.863520Z')
        Measurement.objects.create(metric=Metric.objects.get(id=3), value=5.111,
                                   timestamp='2019-04-11T18:52:17.863520Z')

    def test_HostList_get_queryset(self):
        response = self.client.get(reverse('hosts_list'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"id": 1, "ip": "10.10.10.10", "cpu": "Intel i3", "mac": "00:0A:E6:3E:FD:E1", "memory": "32G",
              "name": "host1",'platform': 'windows'},
             {"id": 2, "ip": "10.10.10.11", "cpu": "Intel i5", "mac": "00:1A:E6:3E:FD:E1", "memory": "16G",
              "name": "host2",'platform': 'windows'},
             {"id": 3, "ip": "10.10.10.12", "cpu": "Intel i7", "mac": "00:2A:E6:3E:FD:E1", "memory": "8G",
              "name": "host3",'platform': 'windows'}]
        )

    def test_HostList_filter_by_query_param(self):
        response = self.client.get(reverse("hosts_list"), {"cpu": "Intel i3"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'cpu': 'Intel i3', 'id': 1, 'ip': '10.10.10.10', 'mac': '00:0A:E6:3E:FD:E1', 'memory': '32G',
              'name': 'host1','platform': 'windows'}]
        )

        response = self.client.get(reverse("hosts_list"), {"ip": "10.10.10.10"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'cpu': 'Intel i3', 'id': 1, 'ip': '10.10.10.10', 'mac': '00:0A:E6:3E:FD:E1', 'memory': '32G',
              'name': 'host1','platform': 'windows'}]
        )

        response = self.client.get(reverse("hosts_list"), {"memory": "32G"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'cpu': 'Intel i3', 'id': 1, 'ip': '10.10.10.10', 'mac': '00:0A:E6:3E:FD:E1', 'memory': '32G',
              'name': 'host1','platform': 'windows'}]
        )

        response = self.client.get(reverse("hosts_list"), {"name": "host1"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'cpu': 'Intel i3', 'id': 1, 'ip': '10.10.10.10', 'mac': '00:0A:E6:3E:FD:E1', 'memory': '32G',
              'name': 'host1','platform': 'windows'}]
        )
        response = self.client.get(reverse("hosts_list"), {"active": "true"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'cpu': 'Intel i5', 'id': 2, 'ip': '10.10.10.11', 'mac': '00:1A:E6:3E:FD:E1', 'memory': '16G',
              'name': 'host2','platform': 'windows'}]
        )

    def test_HostDetail_get(self):
        response = self.client.get(reverse("hosts_detail", kwargs={'pk': 1}), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'cpu': 'Intel i3', 'id': 1, 'ip': '10.10.10.10', 'mac': '00:0A:E6:3E:FD:E1', 'memory': '32G',
             'name': 'host1','platform': 'windows'}
        )

    def test_HostList_post(self):
        response = self.client.post(reverse("hosts_list"),
                                    {"ip": "10.10.10.10", "cpu": "Intel i3", "mac": "00:AA:E6:3E:FD:E1",
                                     "memory": "32G", "name": "host4",'platform': 'windows'}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"id": 4, "ip": "10.10.10.10", "cpu": "Intel i3", "mac": "00:AA:E6:3E:FD:E1", "memory": "32G",
             "name": "host4",'platform': 'windows'}
        )
        response = self.client.post(reverse("hosts_list"),
                                    {"ip": "10.10.10.10", "cpu": "Intel i3", "mac": "00:AA:E6:3E:FD:E1",
                                     "memory": "32G", "name": "host4",'platform': 'windows'}, format="json")
        self.assertEqual(response.status_code, 202)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"id": 4, "ip": "10.10.10.10", "cpu": "Intel i3", "mac": "00:AA:E6:3E:FD:E1", "memory": "32G",
             "name": "host4",'platform': 'windows'}
        )
        response = self.client.post(reverse('hosts_list'), format='json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"ip": ["This field is required."], "cpu": ["This field is required."], 'mac': ['This field is required.'],
             'memory': ['This field is required.'], 'name': ['This field is required.'],'platform': ['This field is required.']}
        )

    def test_MetricDetail_get(self):
        response = self.client.get(reverse("metric_detail", kwargs={'host_name': 'host1','pk':1}), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'id': 1, 'metric_id': 0, 'period_seconds': 5, 'type': 'Type1'}
        )

    def test_MetricList_get_queryset(self):
        response = self.client.get(reverse('metric_list_name', kwargs={'host_name': "host1"}), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"id": 1, 'metric_id': 0, "type": "Type1", "period_seconds": 5},
             {"id": 2, 'metric_id': 0, "type": "mean", "period_seconds": 10}]
        )

        response = self.client.get(reverse('metric_list', kwargs={'host_id': 1}), {'is_custom': "False"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'id': 1, 'metric_id': 0, 'period_seconds': 5, 'type': 'Type1'}]
        )

        response = self.client.get(reverse('metric_list', kwargs={'host_id': 2}), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'id': 3, 'metric_id': 0, 'period_seconds': 5, 'type': 'Type2'},
             {'id': 4, 'metric_id': 3, 'period_seconds': 1, 'type': 'mean'}]
        )

        response = self.client.get(reverse('metric_list', kwargs={'host_id': 2}), {'is_custom': "True"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'id': 4, 'metric_id': 3, 'period_seconds': 1, 'type': 'mean'}]
        )

        response = self.client.get(reverse('metric_list', kwargs={'host_id': 2}), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'id': 3, 'type': 'Type2', 'metric_id': 0, 'period_seconds': 5},
             {'id': 4, 'metric_id': 3, 'period_seconds': 1, 'type': 'mean'}]
        )

        response = self.client.get(reverse('metric_list', kwargs={'host_id': 3}), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            []
        )

    def test_MetricList_post(self):
        response = self.client.post(reverse('metric_list_name', kwargs={'host_name': "host1"}),
                                    {'type': 'memory', "period_seconds": 2}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"id": 5, 'metric_id': 0, "type": "memory", "period_seconds": 2}
        )

        response = self.client.post(reverse('metric_list', kwargs={'host_id': 2}),
                                    {'type': 'disc', "period_seconds": 2}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"id": 6, 'metric_id': 0, "type": "disc", "period_seconds": 2}
        )

        response = self.client.post(reverse('metric_list', kwargs={'host_id': 3}), format='json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'type': ['This field is required.'], 'period_seconds': ['This field is required.']}
        )

        response = self.client.post(reverse('metric_list', kwargs={'host_id': 3}),
                                    {'type': 'UnknownType', 'period_seconds': 2}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"id": 7, 'metric_id': 0, "type": "UnknownType", "period_seconds": 2}
        )
        response = self.client.post(reverse('metric_list', kwargs={'host_id': 1}),
                                    {'type': 'memory', 'period_seconds': 2}, format='json')
        self.assertEqual(response.status_code, 202)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"id": 5, 'metric_id': 0, "type": "memory", "period_seconds": 2}
        )

    def test_MeasurementList_get(self):

        response = self.client.get(reverse('measurement_list', kwargs={'host_name':"host1", 'metric_name':"Type1"}), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"value": 2.201, "timestamp": "2018-04-11T18:52:17.863520Z"},
              {"value": 1.0, "timestamp": "2018-04-11T18:52:17.863018Z"}]
        )
        response = self.client.get(reverse('measurement_list', args=[1, 1]), {'since': "2018-04-11T18:52:17.863519Z"},format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
             [{"value": 2.201, "timestamp": "2018-04-11T18:52:17.863520Z"}]
        )
        response = self.client.get(reverse('measurement_list', args=[2, 4]), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'timestamp': '2019-04-11T18:52:17.863520Z', 'value': 5.111}]

        )

    def test_MeasurementList_post(self):
        response = self.client.post(reverse('measurement_list', args=[1, 1]),
                                    {'value': 11.11, 'timestamp': '2018-04-11T18:52:17.863520Z'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'value': 11.11, 'timestamp': '2018-04-11T18:52:17.863520Z'}
        )

        response = self.client.post(reverse('measurement_list', args=[5, 5]), {'value': 1.0}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'timestamp': ['This field is required.']}
        )

    def test_is_custom(self):
        Metric.objects.create(host=Host.objects.create(ip='10.0.0.1'), type='mean', period_seconds=5)
        metric = Metric.objects.get(id=4)
        response = metric.is_custom
        self.assertTrue(response)
