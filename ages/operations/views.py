from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from sites.models import Site
from .models import Shift
from .serializers import BulkAttendanceSerializer
from .serializers import SiteSerializer, ShiftSerializer

class SiteListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        sites = Site.objects.all()
        return Response(SiteSerializer(sites, many=True).data)

class ShiftBySiteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, site_id):
        shifts = Shift.objects.filter(site_id=site_id)
        return Response(ShiftSerializer(shifts, many=True).data)
    

class BulkAttendanceCreateView(APIView):
    permission_classes = [IsAuthenticated]

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