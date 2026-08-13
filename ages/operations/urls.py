from django.urls import path,include
from .views import (BulkAttendanceCreateView,SiteListAPIView,
                    ShiftBySiteAPIView,UserLocationCreateView, 
                    WorkerPhotoReportCreateView , AdminShiftViewSet)

from rest_framework.routers import DefaultRouter

from .views import AdminShiftViewSet


router = DefaultRouter()

router.register(
    "admin/shifts",
    AdminShiftViewSet,
    basename="admin-shift"
)

urlpatterns = [
    ####Admin CRUD shift####
    path("", include(router.urls)),

    #### Attendance #####
    path("attendance/", BulkAttendanceCreateView.as_view(), name="attendance-bulk"),
    path("sites/", SiteListAPIView.as_view(), name="sites"),
    path("sites/<int:site_id>/shifts/", ShiftBySiteAPIView.as_view(), name="site-shifts"),
    ##### GPS tracking#########
    path("location/", UserLocationCreateView.as_view()),
    ####### worker photos#######
    path("worker-photos/", WorkerPhotoReportCreateView.as_view(), name="worker-photos" ),
    
]