from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .models import InventoryAudit, InventoryRequest, InventoryReceipt
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

######################## Inventory Audit view #########################

@extend_schema(
    request=InventoryAuditSwaggerSerializer,
    responses=InventoryAuditSerializer
)
class InventoryAuditCreateView(CreateAPIView):
    serializer_class = InventoryAuditCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        return {"request": self.request}


@extend_schema(
    responses=InventoryAuditSerializer
)  
class InventoryAuditListView(ListAPIView):
    serializer_class = InventoryAuditSerializer
    permission_classes = [IsAuthenticated]
    queryset = InventoryAudit.objects.all()
    

@extend_schema(
    responses=InventoryAuditSerializer
) 
class InventoryAuditDetailView(RetrieveAPIView):
    serializer_class = InventoryAuditSerializer
    permission_classes = [IsAuthenticated]
    queryset = InventoryAudit.objects.all()


#################################################################
######################## Inventory Request view #########################
################################################################

@extend_schema(
    request=InventoryRequestSwaggerSerializer,
    responses=InventoryRequestSerializer
)
class InventoryRequestCreateView(CreateAPIView):
    serializer_class = InventoryRequestCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}


@extend_schema(
    responses=InventoryRequestSerializer
)
class InventoryRequestListView(ListAPIView):
    serializer_class = InventoryRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = InventoryRequest.objects.all()

@extend_schema(
    responses=InventoryRequestSerializer
)   
class InventoryRequestDetailView(RetrieveAPIView):
    serializer_class = InventoryRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = InventoryRequest.objects.all()


#################################################################
######################## Inventory Reciept view #########################
################################################################

@extend_schema(
    request=InventoryReceiptSwaggerSerializer,
    responses=InventoryReceiptSerializer
)
class InventoryReceiptCreateView(CreateAPIView):
    serializer_class = InventoryReceiptCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}


@extend_schema(
    responses=InventoryReceiptSerializer
)
class InventoryReceiptListView(ListAPIView):
    serializer_class = InventoryReceiptSerializer
    permission_classes = [IsAuthenticated]
    queryset = InventoryReceipt.objects.all()


@extend_schema(
    responses=InventoryReceiptSerializer
)    
class InventoryReceiptDetailView(RetrieveAPIView):
    serializer_class = InventoryReceiptSerializer
    permission_classes = [IsAuthenticated]
    queryset = InventoryReceipt.objects.all()