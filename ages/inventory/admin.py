from django.contrib import admin
from .models import *

admin.site.register(InventoryAudit)
admin.site.register(InventoryAuditItem)
admin.site.register(InventoryAuditImage)

admin.site.register(InventoryRequest)
admin.site.register(InventoryRequestItem)

admin.site.register(InventoryReceipt)
admin.site.register(InventoryReceiptItem)

