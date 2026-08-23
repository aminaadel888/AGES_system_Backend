from django.urls import path, include
from .views import (RegisterView, LoginView ,
                    SupervisorDropdownAPIView,SiteManagerDropdownAPIView,AreaManagerDropdownAPIView,
                    AdminUserViewSet,ChangeOwnPasswordView)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    "admin",
    AdminUserViewSet,
    basename="admin-user"
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path( "supervisors/",SupervisorDropdownAPIView.as_view(), name="supervisor-dropdown"),
    path( "site-managers/",SiteManagerDropdownAPIView.as_view(),name="site-manager-dropdown"),
    path("area-managers/",AreaManagerDropdownAPIView.as_view(), name="area-manager-dropdown"),

    path("change-own-password/",ChangeOwnPasswordView.as_view(),name="change-own-password"),
    ## Admin ##
    path("", include(router.urls)),

]