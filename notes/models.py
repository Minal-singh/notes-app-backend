from django.db import models
import uuid
from customuser.models import CustomUser

COLOR_CHOICES = (
    ("RED","red"),
    ("YELLOW","yellow"),
    ("BLUE","blue"),
    ("GREEN","green")
)

class Folder(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=20,unique=True)
    color = models.CharField(max_length=20,choices=COLOR_CHOICES,default="YELLOW")
    owner = models.ForeignKey(CustomUser,to_field="username",on_delete=models.CASCADE,related_name="folders") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class Note(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    folder = models.ForeignKey(Folder,to_field="name",on_delete=models.SET_NULL,null=True,blank=True)
    owner = models.ForeignKey(CustomUser,to_field="username",on_delete=models.CASCADE,related_name="notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']