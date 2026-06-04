from django.shortcuts import render
from rest_framework import generics
from .models import WeeklyCleaningReport ,WeeklyCleaningReportFile,IncidentReport
from drf_spectacular.utils import extend_schema
from .serializers import (WeeklyCleaningReportCreateSerializer , WeeklyCleaningReportFileSerializer,
                          WeeklyCleaningReportSwaggerSerializer ,IncidentReportSerializer)
from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser
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