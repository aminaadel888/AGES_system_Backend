from django.contrib import admin
from .models import Shift, Attendance, AttendanceRecord
from users.models import User
from .models import WorkerPhotoReport, WorkerPhoto

class AttendanceAdmin(admin.ModelAdmin):
    exclude = ("supervisor",)  # نخفيه من الفورم

    def save_model(self, request, obj, form, change):
        obj.supervisor = request.user 
        super().save_model(request, obj, form, change)


admin.site.register(Shift)
admin.site.register(Attendance , AttendanceAdmin)
admin.site.register(AttendanceRecord)

admin.site.register(WorkerPhotoReport)
admin.site.register(WorkerPhoto)