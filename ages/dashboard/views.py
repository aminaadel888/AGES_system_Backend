from django.contrib.auth import get_user_model
from django.db.models import Sum, Count, Q
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from sites.models import Site
from operations.models import Attendance , AttendanceRecord
from reports.models import IncidentReport, WeeklyCleaningReport

from .serializers import *

User = get_user_model()


######### Overview ############
class AdminDashboardOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Admin only
        if request.user.role != "admin":
            return Response(
                {"detail": "ليس لديك الصلاحيه لاستخدام ال dashboard"},
                status=403
            )

        today = timezone.localdate()

        total_sites = Site.objects.count()

        active_sites = Site.objects.filter(is_active=True).count()

        total_supervisors = User.objects.filter(role="supervisor").count()
        total_managers = User.objects.filter(role="manager").count()
        

        # Today's Attendance

        today_attendance = Attendance.objects.filter(date=today)

        today_attendance_sheets = today_attendance.count()

        attendance_records = AttendanceRecord.objects.filter(attendance__date=today)

        attendance_breakdown = attendance_records.aggregate(
            present=Count(
                "id",
                filter=Q(status="present")
            ),
            absent=Count(
                "id",
                filter=Q(status="absent")
            ),
            leave=Count(
                "id",
                filter=Q(status="leave")
            ),
        )


        total_incidents = IncidentReport.objects.count()

        total_weekly_reports = WeeklyCleaningReport.objects.count()

        data = {
            "total_sites": total_sites,
            "active_sites": active_sites,
            "total_supervisors": total_supervisors,
            "total_managers": total_managers,
            "today_attendance_sheets": today_attendance_sheets,
            "attendance": {
                "present": attendance_breakdown["present"],
                "absent": attendance_breakdown["absent"],
                "leave": attendance_breakdown["leave"],
            },
            "total_incidents": total_incidents,
            "total_weekly_reports": total_weekly_reports,
        }

        serializer = DashboardOverviewSerializer(data)

        return Response(serializer.data)


############## Attendance ############

class AdminDashboardAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Admin only
        if request.user.role != "admin":
            return Response(
                {
                    "detail": "ليس لديك الصلاحيه لاستخدام ال dashboard"
                },
                status=403
            )

        today = timezone.localdate()

        attendance_data = (
            Attendance.objects
            .filter(date=today)
            .select_related("site", "shift")
            .annotate(
                present=Count(
                    "records",
                    filter=Q(records__status="present")
                ),
                absent=Count(
                    "records",
                    filter=Q(records__status="absent")
                ),
                leave=Count(
                    "records",
                    filter=Q(records__status="leave")
                ),
                total_workers=Count("records")
            )
            .order_by("site__name", "shift__name")
        )

        data = []

        for attendance in attendance_data:
            data.append({
                "site_id": attendance.site_id,
                "site_name": attendance.site.name,

                "shift_id": attendance.shift_id,
                "shift_name": attendance.shift.name,

                "date": attendance.date,

                "present": attendance.present,
                "absent": attendance.absent,
                "leave": attendance.leave,
                "total_workers": attendance.total_workers,
            })

        serializer = AttendanceDashboardSerializer(
            data,
            many=True
        )

        return Response(serializer.data)


#########  Incidents ##################
class AdminDashboardIncidentsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardIncidentSerializer

    def get_queryset(self):
        if self.request.user.role != "admin":
            return IncidentReport.objects.none()

        queryset = (
            IncidentReport.objects
            .select_related("site", "reported_by")
            .prefetch_related("images")
        )

        site = self.request.query_params.get("site")
        severity = self.request.query_params.get("severity")
        date = self.request.query_params.get("date")

        if site:
            queryset = queryset.filter(site_id=site)

        if severity:
            queryset = queryset.filter(severity=severity)

        if date:
            queryset = queryset.filter(
                incident_datetime__date=date
            )

        return queryset


############### weekly Reports ####################
class AdminDashboardWeeklyReportsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardWeeklyReportSerializer

    def get_queryset(self):
        if self.request.user.role != "admin":
            return WeeklyCleaningReport.objects.none()

        queryset = (
            WeeklyCleaningReport.objects
            .select_related(
                "site",
                "shift",
                "supervisor"
            )
            .prefetch_related("files")
        )

        site = self.request.query_params.get("site")
        shift = self.request.query_params.get("shift")
        supervisor = self.request.query_params.get("supervisor")
        date = self.request.query_params.get("date")

        if site:
            queryset = queryset.filter(
                site_id=site
            )

        if shift:
            queryset = queryset.filter(
                shift_id=shift
            )

        if supervisor:
            queryset = queryset.filter(
                supervisor_id=supervisor
            )

        if date:
            queryset = queryset.filter(
                report_date=date
            )

        return queryset.order_by("-report_date", "-created_at")

######## Notes ########################################

class AdminDashboardNotesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardNoteSerializer

    def get_queryset(self):
        if self.request.user.role != "admin":
            return Note.objects.none()

        queryset = (
            Note.objects
            .select_related(
                "site",
                "shift",
                "created_by"
            )
        )

        site = self.request.query_params.get("site")
        shift = self.request.query_params.get("shift")
        note_type = self.request.query_params.get("note_type")
        date = self.request.query_params.get("date")

        if site:
            queryset = queryset.filter(site_id=site)

        if shift:
            queryset = queryset.filter(shift_id=shift)

        if note_type:
            queryset = queryset.filter(note_type=note_type)

        if date:
            queryset = queryset.filter(created_at__date=date)

        return queryset.order_by("-created_at")