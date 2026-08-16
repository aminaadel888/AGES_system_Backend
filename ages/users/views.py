from django.shortcuts import render
from rest_framework import generics, status
from .models import User
from .serializers import RegisterSerializer,LoginSerializer,SupervisorDropdownSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
#jwt 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
#permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin

from drf_spectacular.utils import extend_schema


class SupervisorDropdownAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        supervisors = User.objects.filter(
            role__in=["supervisor", "manager"],
            is_active=True
        ).exclude(
            id=request.user.id
        )

        serializer = SupervisorDropdownSerializer(
            supervisors,
            many=True
        )

        return Response(serializer.data)
# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# @extend_schema(
#     request=LoginSerializer,
#     responses={200: LoginSerializer}
# )
class LoginView(APIView):
    
    @extend_schema(
        request=LoginSerializer,
    )

   
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # generate tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "username": user.username,
                    "role": user.role,
                },
                #jwt
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TestAuthView(APIView): 
    permission_classes = [IsAuthenticated] 
    def get(self, request): 
        return Response({ 
            "message": "You are authenticated", 
            "user": request.user.phone 
            })
    
class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({
            "message": "Welcome Admin"
        })
    
from .permissions import IsManager

class ManagerView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        return Response({
            "message": "Manager or Admin access"
        })