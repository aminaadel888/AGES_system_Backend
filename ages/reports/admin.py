from django.contrib import admin
from .models import WeeklyCleaningReport,WeeklyCleaningReportFile,ShiftHandoverReport,ShiftHandoverImage,IncidentImage,IncidentReport

admin.site.register(WeeklyCleaningReport)
admin.site.register(WeeklyCleaningReportFile)

admin.site.register(IncidentReport)
admin.site.register(IncidentImage)


admin.site.register(ShiftHandoverReport)
admin.site.register(ShiftHandoverImage)