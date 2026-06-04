from django.urls import path
from .views import WeeklyCleaningReportCreateView,IncidentReportCreateView

urlpatterns = [
    path("weekly-cleaning/",WeeklyCleaningReportCreateView.as_view(),name="weekly-cleaning-report"),
    path("incident-reports/", IncidentReportCreateView.as_view(),name="incident-report-create")

]