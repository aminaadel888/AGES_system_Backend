from rest_framework import serializers
from .models import AttendanceRecord, Attendance ,Shift
from sites.models import Site
from django.utils import timezone

class WorkerInputSerializer(serializers.Serializer):
    worker_name = serializers.CharField()
    status = serializers.ChoiceField(choices=["present", "absent", "leave"])


class BulkAttendanceSerializer(serializers.Serializer):
    #attendance = serializers.PrimaryKeyRelatedField(queryset=Attendance.objects.all())
    site = serializers.IntegerField()
    shift = serializers.IntegerField()
    workers = WorkerInputSerializer(many=True)

    def validate(self, data):
        site = data["site"]
        shift = data["shift"]

        if not Shift.objects.filter(id=shift, site_id=site).exists():
            raise serializers.ValidationError("Shift does not belong to this site")

        return data

    def create(self, validated_data):
        site = validated_data["site"]
        shift = validated_data["shift"]
        workers = validated_data["workers"]
        #لمنع التكرار
        today = timezone.localdate()

        if Attendance.objects.filter(
            site_id=site,
            shift_id=shift,
            supervisor=self.context["request"].user,
            date=today
        ).exists():
            raise serializers.ValidationError("Attendance already exists for today")

        attendance = Attendance.objects.create(
            site_id=site,
            shift_id=shift,
            supervisor=self.context["request"].user,
            date=today
        )
        
        records = []
        for w in workers:
            records.append(
                AttendanceRecord(
                    attendance=attendance,
                    worker_name=w["worker_name"].strip().title(),
                    status=w["status"]
                )
            )

       

        AttendanceRecord.objects.bulk_create(records)

        return attendance




class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = "__all__"