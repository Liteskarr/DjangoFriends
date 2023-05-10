from drf_spectacular.utils import extend_schema
from rest_framework import generics

import api.models as models
import api.serializers as serializers


@extend_schema(tags=['Users'])
class AllUsers(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.User
