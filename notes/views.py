from django.shortcuts import render
from rest_framework import generics,filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import NotesSerializer,FoldersSerializer,NotesUpdateSerializer
from .models import Note,Folder


class NotesView(generics.ListCreateAPIView):
    serializer_class = NotesSerializer
    queryset = Note.objects.filter(deleted=False)
    permissions_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]

    filterset_fields = ['id','title','description','folder']
    search_fields = ['title','description']
    ordering_fields = ['id','title','description','folder','updated_at','created_at']

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class NotesDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = NotesUpdateSerializer
    queryset = Note.objects.filter(deleted=False)
    permissions_classes = [IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class DeletedNotesView(generics.ListAPIView):
    serializer_class = NotesSerializer
    queryset = Note.objects.filter(deleted=True)
    permissions_classes = [IsAuthenticated,]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class DeletedNotesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotesUpdateSerializer
    queryset = Note.objects.filter(deleted=True)
    permissions_classes = [IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class FolderView(generics.ListCreateAPIView):
    serializer_class = FoldersSerializer
    queryset = Folder.objects.all()
    permissions_classes = [IsAuthenticated,]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class FolderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoldersSerializer
    queryset = Folder.objects.all()
    permissions_classes = [IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)