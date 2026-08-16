from rest_framework import serializers
from reports.models import (IncidentReport, IncidentImage ,
                            WeeklyCleaningReport,WeeklyCleaningReportFile)

from notes.models import Note
from operations.models import WorkerPhotoReport

######### Overview ############
class AttendanceBreakdownSerializer(serializers.Serializer):
    present = serializers.IntegerField()
    absent = serializers.IntegerField()
    leave = serializers.IntegerField()


class DashboardOverviewSerializer(serializers.Serializer):
    total_sites = serializers.IntegerField()
    active_sites = serializers.IntegerField()
    total_supervisors = serializers.IntegerField()
    total_managers=serializers.IntegerField()

    today_attendance_sheets = serializers.IntegerField()
    total_incidents = serializers.IntegerField()
    total_weekly_reports = serializers.IntegerField()

    attendance = AttendanceBreakdownSerializer()

############## Attendance ############
class AttendanceDashboardSerializer(serializers.Serializer):
    site_id = serializers.IntegerField()
    site_name = serializers.CharField()
    shift_id = serializers.IntegerField()
    shift_name = serializers.CharField()
    date = serializers.DateField()

    present = serializers.IntegerField()
    absent = serializers.IntegerField()
    leave = serializers.IntegerField()
    total_workers = serializers.IntegerField()


#########  Incidents ##################

class DashboardIncidentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentImage
        fields = [
            "id",
            "image",
            "uploaded_at",
        ]


class DashboardIncidentSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(
        source="site.name",
        read_only=True
    )

    reported_by_name = serializers.CharField(
        source="reported_by.username",
        read_only=True
    )

    images = DashboardIncidentImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = IncidentReport
        fields = [
            "id",
            "incident_type",
            "description",
            "incident_datetime",
            "latitude",
            "longitude",
            "severity",
            "site",
            "site_name",
            "reported_by",
            "reported_by_name",
            "images",
            "created_at",
        ]

################## weekly Reports ##############

class DashboardWeeklyReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyCleaningReportFile
        fields = [
            "id",
            "file",
            "file_type",
            "uploaded_at",
        ]


class DashboardWeeklyReportSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(
        source="site.name",
        read_only=True
    )

    shift_name = serializers.CharField(
        source="shift.name",
        read_only=True
    )

    supervisor_name = serializers.CharField(
        source="supervisor.username",
        read_only=True
    )

    before_images = serializers.SerializerMethodField()
    after_images = serializers.SerializerMethodField()
    report_files = serializers.SerializerMethodField()

    class Meta:
        model = WeeklyCleaningReport
        fields = [
            "id",
            "site",
            "site_name",
            "shift",
            "shift_name",
            "supervisor",
            "supervisor_name",
            "report_date",
            "created_at",
            "before_images",
            "after_images",
            "report_files",
        ]

    def get_before_images(self, obj):
        files = obj.files.filter(
            file_type=WeeklyCleaningReportFile.BEFORE
        )

        return DashboardWeeklyReportFileSerializer(
            files,
            many=True,
            context=self.context
        ).data

    def get_after_images(self, obj):
        files = obj.files.filter(
            file_type=WeeklyCleaningReportFile.AFTER
        )

        return DashboardWeeklyReportFileSerializer(
            files,
            many=True,
            context=self.context
        ).data

    def get_report_files(self, obj):
        files = obj.files.filter(
            file_type=WeeklyCleaningReportFile.REPORT
        )

        return DashboardWeeklyReportFileSerializer(
            files,
            many=True,
            context=self.context
        ).data


########### Notes ####################################

class DashboardNoteSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(
        source="site.name",
        read_only=True
    )

    shift_name = serializers.CharField(
        source="shift.name",
        read_only=True
    )

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    class Meta:
        model = Note
        fields = [
            "id",
            "site",
            "site_name",
            "shift",
            "shift_name",
            "created_by",
            "created_by_name",
            "note_type",
            "description",
            "created_at",
        ]


########## worker photos ############
class DashboardWorkerPhotoSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source="site.name", read_only=True)
    supervisor_name = serializers.CharField(
        source="supervisor.username",
        read_only=True
    )
    images = serializers.SerializerMethodField()

    class Meta:
        model = WorkerPhotoReport
        fields = [
            "id",
            "site_name",
            "supervisor_name",
            "latitude",
            "longitude",
            "notes",
            "created_at",
            "images",
        ]

    def get_images(self, obj):
        request = self.context.get("request")

        return [
            request.build_absolute_uri(photo.image.url)
            if request else photo.image.url
            for photo in obj.images.all()
        ]