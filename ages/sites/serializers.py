from rest_framework import serializers

from .models import Site


class AdminSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = [
            "id",
            "name",
            "address",
            "latitude",
            "longitude",
            "workers_count",
            "is_active",
        ]
        read_only_fields = ["id"]

    def validate_workers_count(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "عدد العمال داخل الموقع لا يمكن ان يكون بالسالب"
            )

        return value