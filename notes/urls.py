from django.urls import path
from .views import NotesView,NotesDetailView,DeletedNotesView,DeletedNotesDetailView,FolderView,FolderDetailView

urlpatterns = [
    path('notes/', NotesView.as_view()),
    path('notes/<str:id>/',NotesDetailView.as_view()),
    path('deleted-notes/', DeletedNotesView.as_view()),
    path('deleted-notes/<str:id>/',DeletedNotesDetailView.as_view()),
    path('folders/', FolderView.as_view()),
    path('folders/<str:id>/',FolderDetailView.as_view()),
]