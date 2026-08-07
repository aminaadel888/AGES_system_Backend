from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .models import InventoryAudit, InventoryRequest, InventoryReceipt
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from users.permissions import IsAdmin,IsManagerOrSupervisor
from rest_framework.response import Response

######################## Inventory Audit view #########################

@extend_schema(
    request=InventoryAuditSwaggerSerializer,
    responses=InventoryAuditSerializer
)
class InventoryAuditCreateView(CreateAPIView):
    serializer_class = InventoryAuditCreateSerializer
    permission_classes = [IsManagerOrSupervisor]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        audit = serializer.save()

        response_serializer = InventoryAuditSerializer(
            audit,
            context={"request": request}
        )

        return Response(
            response_serializer.data,
            status=201
        )


    
@extend_schema(
    responses=InventoryAuditSerializer
)  
class InventoryAuditListView(ListAPIView):
    serializer_class = InventoryAuditSerializer
    permission_classes = [IsAdmin]
    queryset = InventoryAudit.objects.all()
    

@extend_schema(
    responses=InventoryAuditSerializer
) 
class InventoryAuditDetailView(RetrieveAPIView):
    serializer_class = InventoryAuditSerializer
    permission_classes = [IsAdmin]
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
    permission_classes = [IsManagerOrSupervisor]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_obj = serializer.save()

        return Response(
            InventoryRequestSerializer(
                request_obj,
                context={"request": request}
            ).data,
            status=201
        )
    

@extend_schema(
    responses=InventoryRequestSerializer
)
class InventoryRequestListView(ListAPIView):
    serializer_class = InventoryRequestSerializer
    permission_classes = [IsAdmin]
    queryset = InventoryRequest.objects.all()

@extend_schema(
    responses=InventoryRequestSerializer
)   
class InventoryRequestDetailView(RetrieveAPIView):
    serializer_class = InventoryRequestSerializer
    permission_classes = [IsAdmin]
    queryset = InventoryRequest.objects.all()


#################################################################
######################## Inventory Receipt view  #########################
################################################################

@extend_schema(
    request=InventoryReceiptSwaggerSerializer,
    responses=InventoryReceiptSerializer
)
class InventoryReceiptCreateView(CreateAPIView):
    serializer_class = InventoryReceiptCreateSerializer
    permission_classes = [IsManagerOrSupervisor]

    def create(self, request, *args, **kwargs):
    
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
        receipt = serializer.save()
    
        return Response(
            InventoryReceiptSerializer(
                receipt,
                context={"request": request}
            ).data,
            status=201
        )


@extend_schema(
    responses=InventoryReceiptSerializer
)
class InventoryReceiptListView(ListAPIView):
    serializer_class = InventoryReceiptSerializer
    permission_classes = [IsAdmin]
    queryset = InventoryReceipt.objects.all()


@extend_schema(
    responses=InventoryReceiptSerializer
)    
class InventoryReceiptDetailView(RetrieveAPIView):
    serializer_class = InventoryReceiptSerializer
    permission_classes = [IsAdmin]
    queryset = InventoryReceipt.objects.all()