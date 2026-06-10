from django.shortcuts import render ,get_object_or_404

from rest_framework import generics
from .models import (WeeklyCleaningReport ,WeeklyCleaningReportFile,
                     IncidentReport ,
                     ShiftHandoverReport,ShiftHandoverImage)
from drf_spectacular.utils import extend_schema
from .serializers import (WeeklyCleaningReportCreateSerializer , WeeklyCleaningReportFileSerializer,
                          WeeklyCleaningReportSwaggerSerializer ,IncidentReportSerializer,
                          ShiftHandoverImageSerializer,ShiftHandoverReportSerializer,ShiftHandoverCreateSerializer)
from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from rest_framework.views import APIView

###########################################################################
########################## weekly reports ########################################
############################################################################


@extend_schema(
    request=WeeklyCleaningReportSwaggerSerializer,
    responses={201: WeeklyCleaningReportCreateSerializer},
    summary="Create Weekly Cleaning Report",
    description="Create weekly cleaning report with before images, after images and report files."
)
class WeeklyCleaningReportCreateView(generics.CreateAPIView):
    
    queryset = WeeklyCleaningReport.objects.all()
    serializer_class = WeeklyCleaningReportCreateSerializer

    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        before_images = request.FILES.getlist("before_images")
        after_images = request.FILES.getlist("after_images")
        report_files = request.FILES.getlist("report_files")

        if not report_files:
            return Response(
                {
                    "error": "At least one report file is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not before_images:
            return Response(
                {
                    "error": "At least one before image is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not after_images:
            return Response(
                {
                    "error": "At least one after image is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)
    
    @transaction.atomic
    def perform_create(self, serializer):

        report = serializer.save(
            supervisor=self.request.user
        )

        report_files = self.request.FILES.getlist("report_files")
        before_images = self.request.FILES.getlist("before_images")
        after_images = self.request.FILES.getlist("after_images")
        
        for file in report_files:
            WeeklyCleaningReportFile.objects.create(
                report=report,
                file=file,
                file_type="report"
            )

        for image in before_images:
            WeeklyCleaningReportFile.objects.create(
                report=report,
                file=image,
                file_type="before"
            )

        for image in after_images:
            WeeklyCleaningReportFile.objects.create(
                report=report,
                file=image,
                file_type="after"
            )

    
##############################################


#############################################################################
########################## Incident reports  #########################
#############################################################################

class IncidentReportCreateView(generics.CreateAPIView):

    queryset = IncidentReport.objects.all()
    serializer_class = IncidentReportSerializer

    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

##############################################


#############################################################################
########################## Shift Handover reports   #########################
#############################################################################
@extend_schema(
    summary="Create Shift Handover Report",
    description="Create a new shift handover report with images upload",
    request=ShiftHandoverCreateSerializer,
    responses=ShiftHandoverReportSerializer,
    tags=["Shift Handover"]
)
class ShiftHandoverReportCreateView(generics.CreateAPIView):

    queryset = ShiftHandoverReport.objects.all()
    serializer_class = ShiftHandoverCreateSerializer

    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    @transaction.atomic
    def perform_create(self, serializer):

        report = serializer.save(
            current_supervisor=self.request.user
        )

        images = self.request.FILES.getlist("images")

        if images:
            ShiftHandoverImage.objects.bulk_create([
                ShiftHandoverImage(report=report, image=image)
                for image in images
            ])
            

@extend_schema(
    summary="Confirm Shift Handover Receipt",
    description="Next supervisor confirms receiving the handover report",
    tags=["Shift Handover"]
)
class ShiftHandoverReceiveView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        report = get_object_or_404(ShiftHandoverReport, pk=pk)

        # 1. التأكد إن المستخدم هو المستلم
        if request.user != report.next_supervisor:
            return Response(
                {"error": "You are not allowed to receive this report"},
                status=status.HTTP_403_FORBIDDEN
            )

        # 2. التأكد إن التقرير مش مستلم قبل كده
        if report.is_received:
            return Response(
                {"message": "Already received", "received_at": report.received_at},
                status=status.HTTP_200_OK
            )

        # 3. تحديث البيانات
        report.is_received = True
        report.received_at = timezone.now()
        report.save()

        return Response(
            {
                "message": "Handover received successfully",
                "received_at": report.received_at
            },
            status=status.HTTP_200_OK
        )