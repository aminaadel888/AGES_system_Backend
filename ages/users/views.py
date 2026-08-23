from django.shortcuts import render
from rest_framework import generics, status,viewsets
from rest_framework.decorators import action

from .models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
#jwt 
from rest_framework_simplejwt.tokens import RefreshToken
#permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSiteManager, IsAreaManager ,IsAdmin

from drf_spectacular.utils import extend_schema


class SupervisorDropdownAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        users = User.objects.filter(
            role="supervisor",
            is_active=True
        )

        serializer = UserDropdownSerializer(
            users,
            many=True
        )

        return Response(serializer.data)

class SiteManagerDropdownAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        users = User.objects.filter(
            role="site_manager",
            is_active=True
        )

        serializer = UserDropdownSerializer(
            users,
            many=True
        )

        return Response(serializer.data)

class AreaManagerDropdownAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        users = User.objects.filter(
            role="area_manager",
            is_active=True
        )

        serializer = UserDropdownSerializer(
            users,
            many=True
        )

        return Response(serializer.data)
# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


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
    

class SiteManagerView(APIView):
    permission_classes = [IsSiteManager]
    def get(self, request):
        return Response({
            "message": "Site Manager or Admin access"
        })

class AreaManagerView(APIView):
    permission_classes = [IsAreaManager]
    def get(self, request):
        return Response({
            "message": "Area Manager or Admin access"
        })


#############################################################################
##################### Admin  ##########################
########################################################################################
class AdminUserViewSet(viewsets.ModelViewSet):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return User.objects.all().order_by("id")

    @action(
        detail=True,
        methods=["patch"],
        url_path="change-password"
    )
    def change_password(self, request, pk=None):
        user = self.get_object()

        serializer = AdminChangePasswordSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user.set_password(
            serializer.validated_data["password"]
        )

        user.save()

        return Response(
            {
                "message": "Password changed successfully."
            },
            status=status.HTTP_200_OK
        )


###### change my own password ###########

class ChangeOwnPasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangeOwnPasswordSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = request.user

        user.set_password(
            serializer.validated_data["new_password"]
        )

        user.save()

        return Response(
            {
                "message": "Password changed successfully."
            },
            status=status.HTTP_200_OK
        )