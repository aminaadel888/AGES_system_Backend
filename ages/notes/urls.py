from django.urls import path
from .views import NoteCreateView,NoteListView


urlpatterns = [
   path("create/",NoteCreateView.as_view(),name="note-create"),
   path("list/", NoteListView.as_view(), name="note-list"),

]