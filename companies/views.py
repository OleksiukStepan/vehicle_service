from rest_framework import viewsets

from companies.models import Company
from companies.serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Company model.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
