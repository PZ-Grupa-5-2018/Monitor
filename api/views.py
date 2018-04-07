from django.views.generic import View
from rest_framework import generics

from .models import Measurement
from .serializers import MeasurementSerializer


class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


class HomePageView(View):
    template_name = 'main/index.html'
