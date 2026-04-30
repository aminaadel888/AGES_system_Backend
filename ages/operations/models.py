from django.db import models
from sites.models import Site
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Shift(models.Model):
    SHIFT_TYPES = [
        ("morning", "Morning"),
        ("evening", "Evening"),
        ("night", "Night"),
    ]

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="shifts")

    name = models.CharField(max_length=20, choices=SHIFT_TYPES)

    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ("site", "name")

    def __str__(self):
        return f"{self.site.name} - {self.name}"
    


class Attendance(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="attendances")
    shift = models.ForeignKey("Shift", on_delete=models.CASCADE, related_name="attendances")

    supervisor = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField(default=timezone.localdate)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.shift.site_id != self.site_id:
            raise ValidationError("الشيفت لا ينتمي لهذا الموقع")

    def save(self, *args, **kwargs):
        self.full_clean()  # دي اللي بتشغل validation
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("site", "shift", "date")

    def __str__(self):
        return f"{self.site.name} - {self.shift.name} - {self.date}"
    


class AttendanceRecord(models.Model):

    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("leave", "Leave"),
    ]

    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name="records"
    )

    worker_name = models.CharField(max_length=255)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ("attendance", "worker_name")

    def __str__(self):
        return f"{self.worker_name} - {self.status}"