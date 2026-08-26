from rest_framework import viewsets
from users.permissions import IsAdmin

from .models import Site
from .serializers import AdminSiteSerializer
from django.db.models import Count


class AdminSiteViewSet(viewsets.ModelViewSet):

    queryset = Site.objects.all().order_by("name")
    serializer_class = AdminSiteSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return (
            Site.objects
            .annotate(shifts_count=Count("shifts"))
            .order_by("name")
        )