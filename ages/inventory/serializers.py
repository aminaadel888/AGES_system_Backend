from rest_framework import serializers
from .models import *
from django.db import transaction

######################## Inventory Audit serializers #########################

class InventoryAuditItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryAuditItem
        fields = [
            "item_name",
            "quantity",
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0."
            )
        return value
    

class InventoryAuditImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryAuditImage
        fields = [
            "id",
            "image",
        ]

class InventoryAuditSerializer(serializers.ModelSerializer):

    items = InventoryAuditItemCreateSerializer(
        many=True,
        read_only=True
    )

    images = InventoryAuditImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = InventoryAudit
        fields = [
            "id",
            "site",
            "created_by",
            "audit_date",
            "notes",
            "created_at",
            "items",
            "images",
        ]

        read_only_fields = [
            "created_by",
            "created_at",
        ]

class InventoryAuditCreateSerializer(serializers.ModelSerializer):

    items = InventoryAuditItemCreateSerializer(
        many=True,
        write_only=True
    )

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = InventoryAudit
        fields = [
            "site",
            "audit_date",
            "notes",
            "items",
            "images",
        ]

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Items cannot be empty.")
        return value
    
    def create(self, validated_data):

        items_data = validated_data.pop("items")
        images_data = validated_data.pop("images", [])

        with transaction.atomic():

            audit = InventoryAudit.objects.create(
                created_by=self.context["request"].user,
                **validated_data
            )

            for item in items_data:
                InventoryAuditItem.objects.create(
                    audit=audit,
                    **item
                )

            for image in images_data:
                InventoryAuditImage.objects.create(
                    audit=audit,
                    image=image
                )

        return audit

#################### for swagger ####################################
class InventoryAuditSwaggerSerializer(serializers.Serializer):

    site = serializers.IntegerField()
    audit_date = serializers.DateField()
    notes = serializers.CharField(required=False)

    items = serializers.ListField(
        child=serializers.DictField(),
        required=True
    )

    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )

#################################################################
######################## Inventory Request serializers #########################
################################################################

class InventoryRequestItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryRequestItem
        fields = [
            "item_name",
            "quantity_requested",
        ]   
    
    def validate_quantity_requested(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0."
            )
        return value

class InventoryRequestItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryRequestItem
        fields = [
            "id",
            "item_name",
            "quantity_requested",
        ]


class InventoryRequestSerializer(serializers.ModelSerializer):

    items = InventoryRequestItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = InventoryRequest
        fields = [
            "id",
            "site",
            "requested_by",
            "request_date",
            "notes",
            "created_at",
            "items",
        ]

        read_only_fields = [
            "requested_by",
            "created_at",
        ]


class InventoryRequestCreateSerializer(serializers.ModelSerializer):

    items = InventoryRequestItemCreateSerializer(
        many=True,
        write_only=True
    )

    class Meta:
        model = InventoryRequest
        fields = [
            "site",
            "request_date",
            "notes",
            "items",
        ]

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Items cannot be empty.")
        return value

    def create(self, validated_data):

        items_data = validated_data.pop("items")

        with transaction.atomic():

            request_obj = InventoryRequest.objects.create(
                requested_by=self.context["request"].user,
                **validated_data
            )

            for item in items_data:
                InventoryRequestItem.objects.create(
                    request=request_obj,
                    **item
                )

        return request_obj
    
#################### for swagger ####################################
class InventoryRequestSwaggerSerializer(serializers.Serializer):

    site = serializers.IntegerField()
    request_date = serializers.DateField()
    notes = serializers.CharField(required=False)

    items = serializers.ListField(
        child=serializers.DictField(),
        required=True
    )
    
#################################################################
######################## Inventory Receipt serializers #########################
################################################################
class InventoryReceiptItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryReceiptItem
        fields = [
            "item_name",
            "quantity_received",
        ]

    def validate_quantity_received(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0."
            )
        return value

class InventoryReceiptItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryReceiptItem
        fields = [
            "id",
            "item_name",
            "quantity_received",
        ]

class InventoryReceiptSerializer(serializers.ModelSerializer):

    items = InventoryReceiptItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = InventoryReceipt
        fields = [
            "id",
            "site",
            "received_by",
            "received_date",
            "notes",
            "created_at",
            "items",
        ]

        read_only_fields = [
            "received_by",
            "created_at",
        ]

class InventoryReceiptCreateSerializer(serializers.ModelSerializer):

    items = InventoryReceiptItemCreateSerializer(
        many=True,
        write_only=True
    )

    class Meta:
        model = InventoryReceipt
        fields = [
            "site",
            "received_date",
            "notes",
            "items",
        ]

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Items cannot be empty.")
        return value
    
    def create(self, validated_data):

        items_data = validated_data.pop("items")

        with transaction.atomic():
            receipt = InventoryReceipt.objects.create(
                received_by=self.context["request"].user,
                **validated_data
            )

            for item in items_data:
                InventoryReceiptItem.objects.create(
                    receipt=receipt,
                    **item
                )

        return receipt
    
#################### for swagger ####################################
class InventoryReceiptSwaggerSerializer(serializers.Serializer):

    site = serializers.IntegerField()
    received_date = serializers.DateField()
    notes = serializers.CharField(required=False)

    items = serializers.ListField(
        child=serializers.DictField(),
        required=True
    )