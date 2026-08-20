from django.db import models
from users.models import User
from sites.models import Site
from operations.models import Shift



######################## Inventory Audit #########################

class InventoryAudit(models.Model):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="inventory_audits"
    )

    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        related_name="inventory_audits"
    )


    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="inventory_audits"
    )

    audit_date = models.DateField()

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.site} - {self.audit_date}"


class InventoryAuditItem(models.Model):
    audit = models.ForeignKey(
        InventoryAudit,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item_name = models.CharField(
        max_length=255
    )

    quantity = models.PositiveIntegerField()


    def __str__(self):
        return self.item_name


class InventoryAuditImage(models.Model):
    audit = models.ForeignKey(
        InventoryAudit,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="inventory_audits/%Y/%m/%d/"
    )



#################################################################
######################## Inventory Request #########################
################################################################

class InventoryRequest(models.Model):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="inventory_requests"
    )

    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        related_name="inventory_requests"
    )

    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="inventory_requests"
    )


    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.site} - {self.created_at}"


class InventoryRequestItem(models.Model):
    request = models.ForeignKey(
        InventoryRequest,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item_name = models.CharField(
        max_length=255
    )

    quantity_requested = models.PositiveIntegerField()

    
    def __str__(self):
        return self.item_name
    


#################################################################
######################## Inventory Receipt #########################
################################################################
class InventoryReceipt(models.Model):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="inventory_receipts"
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        related_name="inventory_receipts"
    )


    received_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="inventory_receipts"
    )


    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.site} - {self.received_date}"


class InventoryReceiptItem(models.Model):
    receipt = models.ForeignKey(
        InventoryReceipt,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item_name = models.CharField(
        max_length=255
    )

    quantity_received = models.PositiveIntegerField()


    def __str__(self):
        return self.item_name