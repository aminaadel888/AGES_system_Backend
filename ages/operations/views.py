from typing import Generic
from rest_framework import generics,viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from sites.models import Site
from .models import Shift, Attendance ,AttendanceRecord
from .serializers import BulkAttendanceSerializer ,SiteSerializer, ShiftSerializer,WorkerPhoto,WorkerPhotoReportSerializer, SiteDropdownSerializer,ShiftDropdownSerializer ,AdminShiftSerializer,WorkerPhotoReportCreateSerializer
from drf_spectacular.utils import extend_schema
import json
from django.db import transaction
from rest_framework import status
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError

##################### Admin CRUD shift #############
class AdminShiftViewSet(viewsets.ModelViewSet):
    serializer_class = AdminShiftSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "admin":
            return Shift.objects.none()

        return Shift.objects.select_related(
            "site"
        ).all().order_by("site__name", "start_time")
##############################################################

class SiteListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        sites = Site.objects.all()
        return Response(SiteDropdownSerializer(sites, many=True).data)
    

class ShiftBySiteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def get(self, request, site_id):
        shifts = Shift.objects.filter(site_id=site_id)
        return Response(ShiftDropdownSerializer(shifts, many=True).data)
    

class BulkAttendanceCreateView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=BulkAttendanceSerializer,
    )

    @transaction.atomic
    def post(self, request):

        # Validate site & shift
        serializer = BulkAttendanceSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        # Read workers JSON
        try:
            workers = json.loads(
                request.data.get("workers", "[]")
            )

        except json.JSONDecodeError:
            raise ValidationError(
                "Invalid workers format."
            )


        today = timezone.localdate()


        # At least one worker
        if not workers:
            raise ValidationError(
                "يلزم وجود عامل واحد على الأقل."
            )


        # Prevent duplicate attendance
        if Attendance.objects.filter(
            site_id=serializer.validated_data["site"],
            shift_id=serializer.validated_data["shift"],
            supervisor=request.user,
            date=today
        ).exists():

            return Response(
                {
                    "detail": "Attendance already exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        # Validate workers data and images
        for worker in workers:

            worker_name = worker.get("worker_name")
            worker_status = worker.get("status")
            image_key = worker.get("image_key")


            if not worker_name:
                raise ValidationError(
                    "Worker name is required."
                )


            if not worker_status:
                raise ValidationError(
                    f"Status is missing for {worker_name}"
                )


            if not image_key:
                raise ValidationError(
                    f"Image key is missing for {worker_name}"
                )


            if image_key not in request.FILES:
                raise ValidationError(
                    f"Missing ID image for {worker_name}"
                )



        # Create Attendance
        attendance = Attendance.objects.create(
            site_id=serializer.validated_data["site"],
            shift_id=serializer.validated_data["shift"],
            supervisor=request.user,
            date=today
        )



        # Create Attendance Records
        for worker in workers:

            AttendanceRecord.objects.create(

                attendance=attendance,

                worker_name=worker["worker_name"].strip().title(),

                status=worker["status"],

                national_id_image=request.FILES.get(
                    worker["image_key"]
                )
            )



        return Response(
            {
                "message": "Attendance recorded successfully",
                "attendance_id": attendance.id,
                "workers_count": len(workers)
            },
            status=status.HTTP_201_CREATED
        )
#############################################################################
# ##################### workers Photos ########################
# ############################################################################
class WorkerPhotoReportCreateView(generics.CreateAPIView):

    serializer_class = WorkerPhotoReportCreateSerializer
    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        report = serializer.save()

        response_serializer = WorkerPhotoReportSerializer(
            report,
            context={"request": request}
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
# from django.db import transaction
# from rest_framework.exceptions import ValidationError
# import math
# # --------- helper: distance ----------
# def calculate_distance(lat1, lon1, lat2, lon2):
#     R = 6371  # km

#     dlat = math.radians(lat2 - lat1)
#     dlon = math.radians(lon2 - lon1)

#     a = (
#         math.sin(dlat / 2) ** 2
#         + math.cos(math.radians(lat1))
#         * math.cos(math.radians(lat2))
#         * math.sin(dlon / 2) ** 2
#     )

#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     return R * c


# # --------- helper: nearest site ----------
# def get_nearest_site(lat, lon):
#     sites = Site.objects.filter(is_active=True)

#     nearest_site = None
#     min_distance = float("inf")

#     for site in sites:
#         if site.latitude is None or site.longitude is None:
#             continue

#         distance = calculate_distance(
#             lat, lon,
#             float(site.latitude),
#             float(site.longitude)
#         )

#         if distance < min_distance:
#             min_distance = distance
#             nearest_site = site

#     return nearest_site


# # --------- VIEW ----------
# class WorkerPhotoReportCreateView(generics.CreateAPIView):
#     serializer_class = WorkerPhotoReportSerializer
#     permission_classes = [IsAuthenticated]

#     @transaction.atomic
#     def perform_create(self, serializer):

#         # 1. supervisor = logged-in user
#         supervisor = self.request.user

#         # 2. GPS from frontend
#         try:
#             lat = float(self.request.data.get("latitude"))
#             lon = float(self.request.data.get("longitude"))
#         except (TypeError, ValueError):
#             raise ValidationError("Latitude and Longitude are required and must be numbers")

#         # 3. find nearest site
#         site = get_nearest_site(lat, lon)

#         if not site:
#             raise ValidationError("No nearby site found")

#         # 4. create report
#         report = serializer.save(
#             supervisor=supervisor,
#             site=site,
#             latitude=lat,
#             longitude=lon
#         )

#         # 5. images
#         images = self.request.FILES.getlist("images")

#         if not images:
#             raise ValidationError("At least one image is required")

#         WorkerPhoto.objects.bulk_create([
#             WorkerPhoto(report=report, image=img)
#             for img in images
#         ])
#################################################################
######################## GPS TRACKING #########################
################################################################

from .models import UserLocation, UserLastLocation
from .serializers import UserLocationSerializer

class UserLocationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserLocationSerializer(data=request.data)

        if serializer.is_valid():
            location = serializer.save(user=request.user)
            #update last location    
            UserLastLocation.objects.update_or_create(
                user=request.user,
                defaults={
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                }
            )
            return Response({"message": "Location saved"}, status=201)

        return Response(serializer.errors, status=400)