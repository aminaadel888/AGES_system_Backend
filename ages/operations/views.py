from typing import Generic
from rest_framework import generics
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from sites.models import Site
from .models import Shift
from .serializers import BulkAttendanceSerializer
from .serializers import SiteSerializer, ShiftSerializer,WorkerPhoto,WorkerPhotoReportSerializer, SiteDropdownSerializer,ShiftDropdownSerializer
from drf_spectacular.utils import extend_schema


class SiteListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        sites = Site.objects.all()
        return Response(SiteDropdownSerializer(sites, many=True).data)
    

class ShiftBySiteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, site_id):
        shifts = Shift.objects.filter(site_id=site_id)
        return Response(ShiftDropdownSerializer(shifts, many=True).data)
    

class BulkAttendanceCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=BulkAttendanceSerializer,
    )

    def post(self, request):

        serializer = BulkAttendanceSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            attendance = serializer.save()

            return Response({
                "message": "Attendance recorded successfully",
                "attendance_id": attendance.id
            })

        return Response(serializer.errors, status=400)
#############################################################################
# ##################### workers Photos ########################
# ############################################################################
from django.db import transaction
from rest_framework.exceptions import ValidationError
import math
# --------- helper: distance ----------
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# --------- helper: nearest site ----------
def get_nearest_site(lat, lon):
    sites = Site.objects.filter(is_active=True)

    nearest_site = None
    min_distance = float("inf")

    for site in sites:
        if site.latitude is None or site.longitude is None:
            continue

        distance = calculate_distance(
            lat, lon,
            float(site.latitude),
            float(site.longitude)
        )

        if distance < min_distance:
            min_distance = distance
            nearest_site = site

    return nearest_site


# --------- VIEW ----------
class WorkerPhotoReportCreateView(generics.CreateAPIView):
    serializer_class = WorkerPhotoReportSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):

        # 1. supervisor = logged-in user
        supervisor = self.request.user

        # 2. GPS from frontend
        try:
            lat = float(self.request.data.get("latitude"))
            lon = float(self.request.data.get("longitude"))
        except (TypeError, ValueError):
            raise ValidationError("Latitude and Longitude are required and must be numbers")

        # 3. find nearest site
        site = get_nearest_site(lat, lon)

        if not site:
            raise ValidationError("No nearby site found")

        # 4. create report
        report = serializer.save(
            supervisor=supervisor,
            site=site,
            latitude=lat,
            longitude=lon
        )

        # 5. images
        images = self.request.FILES.getlist("images")

        if not images:
            raise ValidationError("At least one image is required")

        WorkerPhoto.objects.bulk_create([
            WorkerPhoto(report=report, image=img)
            for img in images
        ])
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