from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )
    created_by_id = serializers.IntegerField(
        source="created_by.id",
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

    class Meta:
        model = Note
        fields = [
            "id",
            "site",
            "site_name",
            "shift",
            "shift_name",
            "created_by_id",
            "created_by_name",
            "note_type",
            "description",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "site_name",
            "shift_name",
            "created_by_id",
            "created_by_name",
            "created_at",
        ]

    def validate(self, attrs):
        site = attrs["site"]
        shift = attrs["shift"]

        if shift.site != site:
            raise serializers.ValidationError({
                "shift": "Selected shift does not belong to the selected site."
            })

        return attrs