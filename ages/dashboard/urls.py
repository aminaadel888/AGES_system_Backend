from django.urls import path
from .views import *


urlpatterns = [

    path("overview/", AdminDashboardOverviewView.as_view(), name="admin-dashboard-overview"),
    path("attendance/", AdminDashboardAttendanceView.as_view(), name="admin-dashboard-attendance"),
    path("incidents/", AdminDashboardIncidentsView.as_view(), name="admin-dashboard-incidents"),
    path("weekly-reports/", AdminDashboardWeeklyReportsView.as_view(), name="admin-dashboard-weekly-reports"),
    path("notes/",AdminDashboardNotesView.as_view(),name="admin-dashboard-notes"),
    path( "worker-photos/",DashboardWorkerPhotoListView.as_view(),name="dashboard-worker-photos"),


]