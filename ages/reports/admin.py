from django.contrib import admin
from .models import WeeklyCleaningReport,WeeklyCleaningReportFile

admin.site.register(WeeklyCleaningReport)

admin.site.register(WeeklyCleaningReportFile)
