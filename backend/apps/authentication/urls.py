from django.urls import path
from .views import register, UserInfoView, UserInfoUpdateView
from rest_framework_simplejwt.views import TokenRefreshView
from apps.authentication.views import MyTokenObtainPairView, CaptchaAPIView, ChangePasswordView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('user_info/', UserInfoView.as_view(), name='user'),
    path('user_info/update/', UserInfoUpdateView.as_view(), name='user_update'),
    path('captcha/', CaptchaAPIView.as_view(), name='captcha'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),

]
