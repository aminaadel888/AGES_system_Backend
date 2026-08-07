from django.db import models
from django.conf import settings

from sites.models import Site
from operations.models import Shift

class Note(models.Model):

    NOTE_TYPES = [
        ("workers_shortage", "نقص العمال"),
        ("site_issue", "مشكلة في الموقع"),
        ("materials_shortage", "نقص المواد"),
        ("maintenance_request", "طلب صيانة"),
        ("other", "أخرى"),
    ]

    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    shift = models.ForeignKey(
    Shift,
    on_delete=models.CASCADE,
    related_name="notes"
)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    note_type = models.CharField(
        max_length=50,
        choices=NOTE_TYPES
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.site} - {self.note_type}"