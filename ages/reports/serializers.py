from rest_framework import serializers
from .models import WeeklyCleaningReport,WeeklyCleaningReportFile ,IncidentReport, IncidentImage
from django.utils import timezone

from operations.models import Site
from math import radians, sin, cos, sqrt, atan2


###########################################################################
########################## weekly reports ########################################
############################################################################

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


#############################################################################
########################## Incident reports  #########################
#############################################################################

class IncidentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentImage
        fields = ["id", "image"]


class IncidentReportSerializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    uploaded_images = IncidentImageSerializer(
        source="images",
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
            "images",
            "uploaded_images",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_nearest_site(self, latitude, longitude):

        sites = Site.objects.all()

        nearest_site = None
        min_distance = float("inf")

        for site in sites:

            distance = self.calculate_distance(
                float(latitude),
                float(longitude),
                float(site.latitude),
                float(site.longitude)
            )

            if distance < min_distance:
                min_distance = distance
                nearest_site = site

        return nearest_site

    def calculate_distance(self, lat1, lon1, lat2, lon2):

        R = 6371

        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)

        a = (
            sin(dlat / 2) ** 2
            + cos(radians(lat1))
            * cos(radians(lat2))
            * sin(dlon / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    def create(self, validated_data):

        images = validated_data.pop("images", [])

        request = self.context["request"]

        incident = IncidentReport.objects.create(
            reported_by=request.user,
            site=self.get_nearest_site(
                validated_data["latitude"],
                validated_data["longitude"]
            ),
            **validated_data
        )

        for image in images:
            IncidentImage.objects.create(
                incident=incident,
                image=image
            )

        return incident
    

#################### for swagger ####################################
class IncidentReportSwaggerSerializer(serializers.Serializer):

    incident_type = serializers.ChoiceField(
        choices=[
            ("injury", "إصابة"),
            ("equipment_damage", "تلف معدات"),
            ("site_issue", "مشكلة بالموقع"),
            ("other", "أخرى"),
        ]
    )

    description = serializers.CharField()

    incident_datetime = serializers.DateTimeField()

    latitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    severity = serializers.ChoiceField(
        choices=[
            ("low", "منخفض"),
            ("medium", "متوسط"),
            ("high", "عالي"),
        ]
    )

    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )