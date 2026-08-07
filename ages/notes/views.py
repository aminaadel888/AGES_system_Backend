from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from .models import Note
from .serializers import NoteSerializer


class NoteCreateView(generics.CreateAPIView):

    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Notes"],
        summary="Create a note",
        description="Create a new note for a specific site."
    )
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user
        )

class NoteListView(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.select_related(
            "site",
            "shift",
            "created_by"
        ).all()
