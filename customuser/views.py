from rest_framework import generics,status,views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from .serializers import RegistrationSerializer,EmailVerificationSerializer,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer,ChangePasswordSerializer,UpdateUserSerializer,LogoutSerializer,MyTokenObtainPairSerializer,UserSerializer
from .models import CustomUser
from .utils import Util

class UserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer
    def get_object(self,queryset=None):
        return self.request.user

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny,]

    def post(self,request):
        email = request.data['email']
        instance = CustomUser.objects.filter(email=email,is_verified=False)
        if instance.exists():
            instance.delete()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('mail-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username+',\nUse link below to verify your email \n'+absurl
        data={'email_body':email_body,'to_email':user.email,'email_subject':"Verify your email"}

        Util.send_email(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms="HS256")
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'Email':"Successfully verified, login to continue"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({"Error":"Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)
            
        except jwt.exceptions.DecodeError as identifier:
            return Response({"Error":"Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self,request):
        serializer = self.get_serializer(data=request.data)

        email = request.data.get('email','')

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def get(self,request,uidb64,token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error':'Token is not valid, please request a new one'},status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'success':True,'message':'Credentials Valid','uidb64':uidb64,'token':token},status=status.HTTP_200_OK)
        
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error':'Token is not valid, please request a new one'},status=status.HTTP_401_UNAUTHORIZED) 

class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'Password reset success'},status=status.HTTP_200_OK)

#Change Password View
class ChangePasswordView(generics.UpdateAPIView):

    def get_object(self,queryset=None):
        return self.request.user

    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer

#Update Profile View
class UpdateProfileView(generics.UpdateAPIView):

    def get_object(self,queryset=None):
        return self.request.user

    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)