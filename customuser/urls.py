from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegistrationView,VerifyEmail,SetNewPasswordView,PasswordTokenCheckAPI,RequestPasswordResetEmail,ChangePasswordView,UpdateProfileView,LogoutView,MyTokenObtainPairView,UserView

urlpatterns = [
     path('register/',RegistrationView.as_view(),name="register"),
     path('user/',UserView.as_view(),name="user"),
     path('email-verify/',VerifyEmail.as_view(),name="mail-verify"),
     path('request-reset-email/', RequestPasswordResetEmail.as_view(),
          name="request-reset-email"),
     path('password-reset/<uidb64>/<token>/',
          PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
     path('password-reset-complete', SetNewPasswordView.as_view(),
          name='password-reset-complete'),
     path('change_password/', ChangePasswordView.as_view()),
          path('update_profile/', UpdateProfileView.as_view()),
          path('logout/', LogoutView.as_view()),
     path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]