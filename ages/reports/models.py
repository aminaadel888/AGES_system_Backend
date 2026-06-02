from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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