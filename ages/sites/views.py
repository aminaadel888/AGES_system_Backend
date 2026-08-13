from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Site
from .serializers import AdminSiteSerializer


class AdminSiteViewSet(viewsets.ModelViewSet):

    queryset = Site.objects.all().order_by("name")
    serializer_class = AdminSiteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "admin":
            return Site.objects.none()

        return Site.objects.all().order_by("name")