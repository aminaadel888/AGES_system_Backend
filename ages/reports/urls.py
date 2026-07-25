from django.urls import path
from .views import (WeeklyCleaningReportCreateView,IncidentReportCreateView, 
                    ShiftHandoverReceiveView ,ShiftHandoverReportCreateView ,PendingShiftHandoverListAPIView)

urlpatterns = [
    path("weekly-cleaning/",WeeklyCleaningReportCreateView.as_view(),name="weekly-cleaning-report"),
    
    path("incident-reports/", IncidentReportCreateView.as_view(),name="incident-report-create"),

    path("shift-handovers/",ShiftHandoverReportCreateView.as_view(), name="shift-handover-create"),
    path("shift-handovers/<int:pk>/receive/",ShiftHandoverReceiveView.as_view(),name="shift-handover-receive"),
    path("shift-handover/pending/",PendingShiftHandoverListAPIView.as_view(),name="pending-shift-handover",),

]