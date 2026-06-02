from rest_framework import serializers
from .models import WeeklyCleaningReport,WeeklyCleaningReportFile
from django.utils import timezone

class WeeklyCleaningReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyCleaningReportFile
        fields = [
            "id",
            "file",
            "file_type",
        ]

class WeeklyCleaningReportCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeeklyCleaningReport
        fields = ["site", "shift"]

    def validate(self, attrs):

        site = attrs["site"]
        shift = attrs["shift"]

    #### shift validation ########    

        if shift.site_id != site.id:
            raise serializers.ValidationError(
                "Selected shift does not belong to selected site."
            )
       
    #### date validation ########
    
        today = timezone.localdate()

        if today.weekday() != 5:
            raise serializers.ValidationError(
                "Weekly cleaning reports can only be created on Saturday."
            )
        
    ##### repeating validation #####
        if WeeklyCleaningReport.objects.filter(
            site=site,
            shift=shift,
            report_date=today
        ).exists():
            raise serializers.ValidationError(
                "A report already exists for this site and shift today."
            )
        
        return attrs
    

##### for swagger #######################################
class WeeklyCleaningReportSwaggerSerializer(serializers.Serializer):
    site = serializers.IntegerField()
    shift = serializers.IntegerField()

    report_files = serializers.ListField(
        child=serializers.FileField(),
        required=True
    )

    before_images = serializers.ListField(
        child=serializers.FileField(),
        required=True
    )

    after_images = serializers.ListField(
        child=serializers.FileField(),
        required=True
    )

    
##############################################