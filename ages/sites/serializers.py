from rest_framework import serializers

from .models import Site


class AdminSiteSerializer(serializers.ModelSerializer):

    shifts_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Site
        fields = [
            "id",
            "name",
            "address",
            "latitude",
            "longitude",
            "workers_count",
            "break_workers_count",
            "reserve_workers_count",
            "site_manager",
            "area_manager",
            "is_active",
            "shifts_count",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        workers_count = attrs.get("workers_count", 0)
        break_workers_count = attrs.get("break_workers_count", 0)
        reserve_workers_count = attrs.get("reserve_workers_count", 0)

        if workers_count < 0:
            raise serializers.ValidationError(
                "عدد العمال داخل الموقع لا يمكن أن يكون بالسالب"
            )

        if break_workers_count < 0:
            raise serializers.ValidationError(
                "عدد عمال الراحات لا يمكن أن يكون بالسالب"
            )

        if reserve_workers_count < 0:
            raise serializers.ValidationError(
                "عدد العمال الاحتياطي لا يمكن أن يكون بالسالب"
            )

        return attrs