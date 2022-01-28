from rest_framework import serializers
from .models import Folder,Note 

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id','title','description','folder','created_at','updated_at']

class NotesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id','title','description','folder','deleted','created_at','updated_at']

class FoldersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id','name','created_at','color']