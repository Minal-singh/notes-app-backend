from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser,BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(max_length=250,unique=True)
    username = models.CharField(max_length=50,unique=True)
    profile_pic = models.ImageField(null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }