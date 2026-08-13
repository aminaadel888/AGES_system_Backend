from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminSiteViewSet

router = DefaultRouter()

router.register(
    "admin",
    AdminSiteViewSet,
    basename="admin-site"
)

urlpatterns = [
    path("", include(router.urls)),
]