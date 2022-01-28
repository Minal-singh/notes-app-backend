from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","username","email","profile_pic"]

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=60,min_length=6,write_only=True,required=True)
    password2 = serializers.CharField(max_length=60,min_length=6,write_only=True,required=True)

    class Meta:
        model = CustomUser
        fields = ('email','username','password','password2')
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})

        if not attrs['username'].isalnum():
            raise serializers.ValidationError(
                {"username":"Username must be alphanumeric(A-Za-z0-9)"}
            )

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['email'],validated_data['username'],     
        password = validated_data['password'] )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        user = CustomUser.objects.get(email=attrs['email'])
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        return super().validate(attrs)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=1000)

    class Meta:
        model = CustomUser
        fields = ['token']

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6,max_length=60,write_only=True,required=True)
    password2 = serializers.CharField(min_length=6,max_length=60,write_only=True,required=True)
    token = serializers.CharField(write_only=True,required=True)
    uidb64 = serializers.CharField(write_only=True,required=True)

    class Meta:
        fields=['password','password2','token','uidb64']

    def validate(self,attrs):
        try:
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password":"Password fields didn't match."})

            passsword=attrs.get('password')
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid',401)

            user.set_password(passsword)
            user.save()

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid',401)

        return attrs

#Change Password Serializer
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    password2 = serializers.CharField(write_only=True,required=True)
    old_password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password','password','password2')
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})
        return attrs

    def validate_old_password(self,value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password":"Old Password is not correct"})
        return value

    def update(self,instance,validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()
        return instance


#Update Profile Serializer
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username',)

    def validate_username(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.username = validated_data['username']

        instance.save()

        return instance

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self,attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            return Response(status=status.HTTP_205_RESET_CONTENT)