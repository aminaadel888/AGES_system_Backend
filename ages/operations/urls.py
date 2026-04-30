from django.urls import path
from .views import BulkAttendanceCreateView,SiteListAPIView,ShiftBySiteAPIView

urlpatterns = [
    path("attendance/bulk/", BulkAttendanceCreateView.as_view(), name="attendance-bulk"),
    path("sites/", SiteListAPIView.as_view(), name="sites"),
    path("sites/<int:site_id>/shifts/", ShiftBySiteAPIView.as_view(), name="site-shifts"),
]