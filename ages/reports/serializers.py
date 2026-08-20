from rest_framework import serializers
from .models import (WeeklyCleaningReport,WeeklyCleaningReportFile ,IncidentReport, 
                     IncidentImage,ShiftHandoverReport, ShiftHandoverImage)
from django.utils import timezone

from operations.models import Site
from math import radians, sin, cos, sqrt, atan2

from users.models import User
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

        # if today.weekday() != 5:
        #     raise serializers.ValidationError(
        #         "Weekly cleaning reports can only be created on Saturday."
        #     )
        
    ##### repeating validation #####
        if WeeklyCleaningReport.objects.filter(
            site=site,
            shift=shift,
            report_date=today
        ).exists():
            raise serializers.ValidationError(
                "يوجد بالفعل تقرير لهذا الموقع وهذا الشيفت اليوم."
            )


    #### image validation ######    
        ALLOWED_FILE_TYPES = [
         # Images
            "image/jpeg",
            "image/png",
            "image/jpg",
            "image/webp",

        # PDF
            "application/pdf",

        # Excel
            "application/vnd.ms-excel", 
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ]

        request = self.context["request"]

        for field_name in ["report_files", "before_images", "after_images"]:
            files = request.FILES.getlist(field_name)

            for file in files:

                if field_name == "report_files":
                    allowed_types = ALLOWED_FILE_TYPES
                else:
                    allowed_types = [
                        "image/jpeg",
                        "image/png",
                        "image/jpg",
                        "image/webp",
                    ]

                if file.content_type not in allowed_types:
                    raise serializers.ValidationError(
                        {
                            field_name: "Invalid file type."
                        }
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

        sites = Site.objects.filter(is_active=True)

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

        site = self.get_nearest_site(
            validated_data["latitude"],
            validated_data["longitude"]
        )

        if site is None:
            raise serializers.ValidationError({
                "site":" تعذر تحديد الموقع بناءً على إحداثيات نظام تحديد المواقع العالمي (GPS) المقدمة."
            })

        incident = IncidentReport.objects.create(
            reported_by=request.user,
            site=site,
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

    ##########################################################################################
    


 ###########################################################################
########################## Shift Handover reports ########################################
############################################################################

class ShiftHandoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftHandoverImage
        fields = ["id", "image"]


class ShiftHandoverReportSerializer(serializers.ModelSerializer):

    images = ShiftHandoverImageSerializer(
        many=True,
        read_only=True
    )

    site_name = serializers.CharField(
        source="site.name",
        read_only=True
    )

    shift_name = serializers.CharField(
        source="shift.name",
        read_only=True
    )

    current_supervisor_name = serializers.CharField(
        source="current_supervisor.username",
        read_only=True
    )

    next_supervisor_name = serializers.CharField(
        source="next_supervisor.username",
        read_only=True
    )

    class Meta:
        model = ShiftHandoverReport
        fields = [
            "id",

            "site",
            "site_name",

            "shift",
            "shift_name",

            "current_supervisor",
            "current_supervisor_name",

            "next_supervisor",
            "next_supervisor_name",

            "site_status",
            "completed_work",
            "remaining_work",
            "workers_count",
            "ongoing_issues",
            "handover_method",
            "is_received",
            "received_at",
            "created_at",
            "images",
        ]
        read_only_fields = [
            "current_supervisor",
            "is_received",
            "received_at",
            "created_at",
        ]


class ShiftHandoverCreateSerializer(serializers.ModelSerializer):

    next_supervisor = serializers.PrimaryKeyRelatedField(
    queryset=User.objects.filter(
        role__in=["supervisor", "manager"],
        is_active=True
        ),
        required=False,
        allow_null=True
    )

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = ShiftHandoverReport
        fields = [
            "site",
            "shift",
            "next_supervisor",
            "site_status",
            "completed_work",
            "remaining_work",
            "workers_count",
            "ongoing_issues",
            "handover_method",
            "images",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            self.fields["next_supervisor"].queryset = (
                User.objects.filter(
                    role__in=["supervisor", "manager"],
                    is_active=True
                ).exclude(
                    id=request.user.id
                )
            )

    def create(self, validated_data):
        images = validated_data.pop("images", [])

        report = ShiftHandoverReport.objects.create(
            next_supervisor=validated_data.pop("next_supervisor", None),
            **validated_data
        )

        for image in images:
            ShiftHandoverImage.objects.create(
                report=report,
                image=image
            )

        return report

    def validate(self, attrs):
        request = self.context.get("request")

        site = attrs.get("site")
        shift = attrs.get("shift")
        next_supervisor = attrs.get("next_supervisor")
        handover_method = attrs.get("handover_method")

        if shift.site != site:
            raise serializers.ValidationError({
                "shift": "الوردية المختارة لا تتبع الموقع المختار."
            })

        if handover_method == "direct":
            if not next_supervisor:
                raise serializers.ValidationError({
                    "next_supervisor":
                    "يجب اختيار المشرف المستلم عند التسليم المباشر."
                })

            if next_supervisor.role not in ["supervisor", "manager"]:
                raise serializers.ValidationError({
                    "next_supervisor":
                    "يجب أن يكون المشرف المستلم مشرفًا أو مديرًا."
                })

            if request and next_supervisor == request.user:
                raise serializers.ValidationError({
                    "next_supervisor":
                    "لا يمكنك اختيار نفسك كمشرف مستلم."
                })

        elif handover_method == "without_receiving":

            if next_supervisor:
                raise serializers.ValidationError({
                    "next_supervisor":
                    "لا يجب اختيار مشرف مستلم عند اختيار التسليم بدون استلام مباشر."
                })


        return attrs