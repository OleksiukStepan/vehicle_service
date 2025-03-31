from django.urls import path, include
from rest_framework.routers import DefaultRouter

from companies.views import CompanyViewSet

router = DefaultRouter()
router.register(r"companies", CompanyViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "companies"
