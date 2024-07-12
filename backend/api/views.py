from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note


# Views for Notes

# ListCreateAPIView:
# List all of the notes a User has created
# create a new note
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    # set so only the current user can view/create
    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        # if the serializer passed all the fields
        if serializer.is_valid():
            # because the author was set to read only 
            serializer.save(author=self.request.user) 
        else:
            print(serializer.errors)

    # ** Technically, we can leave generic views as is, 
    #    only needing to have serializer_class, permission class, and queryset.
    #    But here we are overiding specific methods to add extra functionality.


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


# Views for creting Users
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]