from django.db import models
from sites.models import Site
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

######################## ATTENDANCE SYSTEM #########################
class Shift(models.Model):
    SHIFT_TYPES = [
        ("morning", "Morning"),
        ("evening", "Evening"),
        ("night", "Night"),
    ]

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="shifts")

    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervised_shifts"
    )


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

    supervisor = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
)

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
        ("present", "حاضر"),
        ("absent", "غائب"),

    ]
        
    
    ABSENCE_REASON_CHOICES = [
        ("with_permission", "غائب باذن"),
        ("without_permission", "غائب بدون اذن"),
        ("sick", "إجازة مرضية"),
        ("annual", "إجازة سنوية"),
        ("other", "إجازة أخرى"),
    ]


    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name="records"
    )

    worker_name = models.CharField(max_length=255)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    absence_reason = models.CharField(
        max_length=20,
        choices=ABSENCE_REASON_CHOICES,
        blank=True,
        null=True
    )

    worker_image = models.ImageField(
        upload_to="attendance/worker_images/%Y/%m/%d/",
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ("attendance", "worker_name")


    def __str__(self):
        return f"{self.worker_name} - {self.status}"

    
########## workers photos #############

class WorkerPhotoReport(models.Model):

    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="worker_photo_reports"
    )

    shift = models.ForeignKey(
        "Shift",
        on_delete=models.CASCADE,
        related_name="worker_photo_reports"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.site.name} - {self.created_at}"


class WorkerPhoto(models.Model):

    IMAGE_TYPE_CHOICES = [
        ("worker", "Worker"),
        ("report", "Report"),
    ]

    report = models.ForeignKey(
        WorkerPhotoReport,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="worker_photos/%Y/%m/%d/"
    )

    image_type = models.CharField(
        max_length=20,
        choices=IMAGE_TYPE_CHOICES
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Photo {self.id} - {self.image_type}"
#################################################################
######################## GPS TRACKING #########################
################################################################


class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="locations")
    latitude = models.FloatField()
    longitude = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - ({self.latitude}, {self.longitude})"
    

#save last location for dashboard
class UserLastLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user} - last location"