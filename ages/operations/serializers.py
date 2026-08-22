from rest_framework import serializers
from .models import AttendanceRecord, Attendance ,Shift,WorkerPhotoReport,WorkerPhoto,UserLocation
from sites.models import Site
from django.utils import timezone
############## Admin CRUD shift ##############

class AdminShiftSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(
        source="site.name",
        read_only=True
    )

    class Meta:
        model = Shift
        fields = [
            "id",
            "site",
            "site_name",
            "name",
            "start_time",
            "end_time",
        ]
        read_only_fields = ["id", "site_name"]

    
################################################################


class BulkAttendanceSerializer(serializers.Serializer):

    site = serializers.IntegerField()
    shift = serializers.IntegerField()

    def validate(self, data):

        site = data["site"]
        shift = data["shift"]

        if not Shift.objects.filter(
            id=shift,
            site_id=site
        ).exists():

            raise serializers.ValidationError(
                "هذا الشيفت غير تابع للموقع"
            )

        return data

class WorkerInputSerializer(serializers.Serializer):

    worker_name = serializers.CharField()

    status = serializers.ChoiceField(
        choices=AttendanceRecord.STATUS_CHOICES
    )

    absence_reason = serializers.ChoiceField(
        choices=AttendanceRecord.ABSENCE_REASON_CHOICES,
        required=False,
        allow_null=True
    )

    image_key = serializers.CharField(
        required=False,
        allow_blank=True
    )

    def validate(self, data):

        status = data["status"]
        absence_reason = data.get("absence_reason")
        image_key = data.get("image_key")

        if status == "present":

            if not image_key:
                raise serializers.ValidationError({
                    "image_key": "صورة العامل مطلوبة للعامل الحاضر."
                })

            if absence_reason:
                raise serializers.ValidationError({
                    "absence_reason": "لا يمكن تحديد سبب غياب للعامل الحاضر."
                })

        elif status == "absent":

            if not absence_reason:
                raise serializers.ValidationError({
                    "absence_reason": "يجب اختيار سبب الغياب."
                })

            if image_key:
                raise serializers.ValidationError({
                    "image_key": "لا يجب إرسال صورة للعامل الغائب."
                })

        return data
#################################################################

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = "__all__"
######### dropdowns ####
class SiteDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ["id", "name"]

class ShiftDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ["id", "name"]
########### worker photo ########

class WorkerPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkerPhoto
        fields = [
            "id",
            "image",
            "image_type",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "uploaded_at",
        ]


class WorkerPhotoReportSerializer(serializers.ModelSerializer):

    images = WorkerPhotoSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = WorkerPhotoReport
        fields = [
            "id",
            "supervisor",
            "site",
            "shift",
            "created_at",
            "images",
        ]

        read_only_fields = [
            "supervisor",
            "created_at",
        ]

class WorkerPhotoReportCreateSerializer(serializers.ModelSerializer):

    
    worker_images = serializers.ListField(
        child=serializers.ImageField(),
        required=True,
        write_only=True
    )

    report_images = serializers.ListField(
        child=serializers.ImageField(),
        required=True,
        write_only=True
    )

    class Meta:
        model = WorkerPhotoReport
        fields = [
            "site",
            "shift",
            "worker_images",
            "report_images",
        ]

    def validate_worker_images(self, value):
        if not value:
            raise serializers.ValidationError(
                "يجب رفع صورة واحدة على الأقل للعمال."
            )

        return value

    def validate_report_images(self, value):
        if not value:
            raise serializers.ValidationError(
                "يجب رفع صورة واحدة على الأقل للتقرير."
            )

        return value

    def validate(self, attrs):

        site = attrs.get("site")
        shift = attrs.get("shift")

        if shift.site != site:
            raise serializers.ValidationError({
                "shift":
                "الوردية المختارة لا تتبع الموقع المختار."
            })

        return attrs
    def create(self, validated_data):

        worker_images = validated_data.pop("worker_images", [])
        report_images = validated_data.pop("report_images", [])

        report = WorkerPhotoReport.objects.create(
            supervisor=self.context["request"].user,
            **validated_data
        )

        for image in worker_images:
            WorkerPhoto.objects.create(
                report=report,
                image=image,
                image_type="worker"
            )

        for image in report_images:
            WorkerPhoto.objects.create(
                report=report,
                image=image,
                image_type="report"
            )

        return report

#################################################################
######################## GPS TRACKING #########################
################################################################

class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ["id", "latitude", "longitude"]