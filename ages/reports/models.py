from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
from sites.models import Site
from users.models import User

###########################################################################
########################## weekly reports ########################################
############################################################################

class WeeklyCleaningReport(models.Model):
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weekly_cleaning_reports")

    site = models.ForeignKey("sites.Site", on_delete=models.CASCADE, related_name="weekly_cleaning_reports")


    shift = models.ForeignKey("operations.Shift", on_delete=models.CASCADE, related_name="weekly_cleaning_reports")

    #notes = models.TextField(blank=True)

    report_date = models.DateField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.id}"
    

class WeeklyCleaningReportFile(models.Model):

    REPORT = "report"
    BEFORE = "before"
    AFTER = "after"
    

    FILE_TYPE_CHOICES = [
        (REPORT, "Report"),
        (BEFORE, "Before"),
        (AFTER, "After"),
        
    ]

    report = models.ForeignKey(
        WeeklyCleaningReport,
        on_delete=models.CASCADE,
        related_name="files"
    )

    file = models.FileField(upload_to="weekly_reports/%Y/%m/%d/")

    file_type = models.CharField(
        max_length=10,
        choices=FILE_TYPE_CHOICES
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type} - {self.report_id}"
    
##########################################################################################
    


 ###########################################################################
########################## Incident reports ########################################
############################################################################

class IncidentReport(models.Model):

    INCIDENT_TYPES = [
        ("injury", "إصابة"),
        ("equipment_damage", "تلف معدات"),
        ("site_issue", "مشكلة بالموقع"),
        ("other", "أخرى"),
    ]

    SEVERITY_LEVELS = [
        ("low", "منخفض"),
        ("medium", "متوسط"),
        ("high", "عالي"),
    ]

    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="incident_reports"
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incident_reports"
    )

    incident_type = models.CharField(
        max_length=30,
        choices=INCIDENT_TYPES
    )

    description = models.TextField(verbose_name="وصف الحادث")

    incident_datetime = models.DateTimeField()

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_LEVELS
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
 

    def __str__(self):
        return f"{self.get_incident_type_display()} - {self.id}"


class IncidentImage(models.Model):

    incident = models.ForeignKey(
        IncidentReport,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="incident_reports/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Image {self.id}"
    
##########################################################################################
    


 ###########################################################################
########################## Shift Handover reports ##################################
############################################################################

class ShiftHandoverReport(models.Model):

    SITE_STATUS_CHOICES = [
        ("clean", "نظيف"),
        ("follow_up", "يحتاج متابعه"),
        ("incomplete", "غير مكتمل"),
    ]

    HANDOVER_METHODS = [
        ("direct", "تسليم مباشر"),
        ("without_receiving", "بدون تسليم مباشر"),
    ]

    shift = models.ForeignKey(
        "operations.Shift",
        on_delete=models.CASCADE,
        related_name="handover_reports"
    )

    current_supervisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_handovers"
    )

    next_supervisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_handovers"
    )

    site_status = models.CharField(
        max_length=20,
        choices=SITE_STATUS_CHOICES
    )

    completed_work = models.TextField()

    remaining_work = models.TextField()

    workers_count = models.PositiveIntegerField()

    ongoing_issues = models.TextField(
        blank=True,
        null=True
    )

    handover_method = models.CharField(
        max_length=30,
        choices=HANDOVER_METHODS
    )

    is_received = models.BooleanField(
        default=False
    )

    received_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Handover #{self.id} - {self.shift.site.name}"


class ShiftHandoverImage(models.Model):

    report = models.ForeignKey(
        ShiftHandoverReport,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="shift_handover/%Y/%m/%d/"
    )

    def __str__(self):
        return f"Image {self.id} for Report {self.report.id}"

