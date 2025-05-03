from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from django.http import HttpResponse
from django.conf import settings

from PIL import Image, ImageDraw, ImageFont
import random
import io

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    captcha = request.data.get('captcha')
    session_captcha = settings.CAPTCHA

    if not captcha or captcha.lower() != session_captcha.lower():
        return Response({'error': 'Invalid captcha'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        # 从请求中获取验证码
        captcha = request.data.get('captcha', None)
        session_captcha = settings.CAPTCHA

        # 验证验证码
        if not captcha or captcha.lower() != session_captcha.lower():
            return Response({'error': 'Invalid captcha'}, status=status.HTTP_400_BAD_REQUEST)

        # 如果验证码正确，继续处理登录请求
        return super().post(request, *args, **kwargs)


class UserInfoView(APIView):
    def get(self, request):
        # 从请求头中获取 Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise APIException("No Authorization header provided")

        # 提取 token
        try:
            token = auth_header.split(' ')[1]
            user_info = UntypedToken(token)
        except IndexError:
            raise APIException("Invalid Authorization header format")

        # 获取 user 实例
        try:
            user_id = user_info['user_id']
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise APIException("User not found")

        print(user)

        # 返回用户信息
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


# 更新用户信息
class UserInfoUpdateView(APIView):
    def post(self, request):
        # 从请求头中获取 Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise APIException("No Authorization header provided")

        # 提取 token
        try:
            token = auth_header.split(' ')[1]
            user_info = UntypedToken(token)
        except IndexError:
            raise APIException("Invalid Authorization header format")

        # 获取 user 实例
        try:
            user_id = user_info['user_id']
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise APIException("User not found")

        # 更新用户信息
        user.email = request.data.get('email')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.save()

        # 返回用户信息
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


class CaptchaAPIView(APIView):

    def get(self, request):
        chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        captcha_text = ''.join(random.choice(chars) for _ in range(4))
        # request.session['captcha'] = captcha_text
        settings.CAPTCHA = captcha_text

        # 保存验证码到 session


        # 调整图像尺寸
        image_size = (50, 20)  # 宽度160px, 高度60px
        font_size = 18  # 字体大小

        image = Image.new('RGB', image_size, color=(255, 255, 255))
        draw = ImageDraw.Draw(image)

        # 加载字体，设置字体大小
        try:
            font = ImageFont.truetype("arial", font_size)
        except IOError:
            font = ImageFont.load_default()

        # 计算文本位置
        text_width, text_height = draw.textsize(captcha_text, font=font)
        text_x = (image_size[0] - text_width) / 2
        text_y = (image_size[1] - text_height) / 2

        draw.text((text_x, text_y), captcha_text, fill=(0, 0, 0), font=font)

        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)

        return HttpResponse(buffer.getvalue(), content_type='image/jpeg')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get('new_password')

        request.user.set_password(new_password)
        request.user.save()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
