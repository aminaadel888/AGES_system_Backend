from django.urls import path
from .views import NoteCreateView


urlpatterns = [
   path("create/",NoteCreateView.as_view(),name="note-create"),

]