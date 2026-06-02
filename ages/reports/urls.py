from django.urls import path
from .views import WeeklyCleaningReportCreateView

urlpatterns = [
    path("weekly-cleaning/",WeeklyCleaningReportCreateView.as_view(),name="weekly-cleaning-report"),
]