from rest_framework import serializers
from .models import AttendanceRecord, Attendance ,Shift,WorkerPhotoReport,WorkerPhoto
from sites.models import Site
from django.utils import timezone

# class WorkerInputSerializer(serializers.Serializer):
#     worker_name = serializers.CharField()
#     status = serializers.ChoiceField(choices=["present", "absent", "leave"])
#     national_id_image = serializers.ImageField(
#         required=False,
#         allow_null=True
#     )


class BulkAttendanceSerializer(serializers.Serializer):
    #attendance = serializers.PrimaryKeyRelatedField(queryset=Attendance.objects.all())
    site = serializers.IntegerField()
    shift = serializers.IntegerField()
    # workers = WorkerInputSerializer(many=True)

    def validate(self, data):
        site = data["site"]
        shift = data["shift"]

        if not Shift.objects.filter(id=shift, site_id=site).exists():
            raise serializers.ValidationError("Shift does not belong to this site")

        return data

    # def create(self, validated_data):
    #     site = validated_data["site"]
    #     shift = validated_data["shift"]
    #     workers = validated_data["workers"]
    #     #لمنع التكرار
    #     today = timezone.localdate()

    #     if Attendance.objects.filter(
    #         site_id=site,
    #         shift_id=shift,
    #         supervisor=self.context["request"].user,
    #         date=today
    #     ).exists():
    #         raise serializers.ValidationError("Attendance already exists for today")

    #     attendance = Attendance.objects.create(
    #         site_id=site,
    #         shift_id=shift,
    #         supervisor=self.context["request"].user,
    #         date=today
    #     )
        
    #     for w in workers:
    #         AttendanceRecord.objects.create(
    #             attendance=attendance,
    #             worker_name=w["worker_name"].strip().title(),
    #             status=w["status"],
    #             national_id_image=w.get("national_id_image")
    #         )


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
        fields = ["id", "image"]

class WorkerPhotoReportSerializer(serializers.ModelSerializer):

    images = WorkerPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = WorkerPhotoReport
        fields = "__all__"
        read_only_fields = ["supervisor",
                            "site",
                            "latitude", 
                            "longitude"
                            ]

#################################################################
######################## GPS TRACKING #########################
################################################################

from .models import UserLocation

class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ["id", "latitude", "longitude", "site"]