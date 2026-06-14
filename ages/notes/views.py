from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from .models import Note
from .serializers import NoteSerializer


@extend_schema(
    tags=["Notes"],
    summary="Create a note",
    description="Create a new note for a specific site."
)

class NoteCreateView(generics.CreateAPIView):

    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user
        )