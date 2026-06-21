from django.urls import path
from .views import *


urlpatterns = [

    path("audits/", InventoryAuditListView.as_view()),
    path("audits/create/", InventoryAuditCreateView.as_view()),
    path("audits/<int:pk>/",InventoryAuditDetailView.as_view()),

    path("request/", InventoryRequestListView.as_view()),
    path("request/create/", InventoryRequestCreateView.as_view()),
    path("request/<int:pk>/",InventoryRequestDetailView.as_view()),


    path("receipt/", InventoryReceiptListView.as_view()),
    path("receipt/create/", InventoryReceiptCreateView.as_view()),
    path("receipt/<int:pk>/",InventoryReceiptDetailView.as_view()),
    

]