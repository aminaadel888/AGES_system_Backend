from django.urls import path
from .views import (WeeklyCleaningReportCreateView,IncidentReportCreateView, 
                    ShiftHandoverReceiveView ,ShiftHandoverReportCreateView)

urlpatterns = [
    path("weekly-cleaning/",WeeklyCleaningReportCreateView.as_view(),name="weekly-cleaning-report"),
    
    path("incident-reports/", IncidentReportCreateView.as_view(),name="incident-report-create"),

    path("shift-handovers/",ShiftHandoverReportCreateView.as_view(), name="shift-handover-create"),
    path("shift-handovers/<int:pk>/receive/",ShiftHandoverReceiveView.as_view(),name="shift-handover-receive"),

]