from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Image
from .serializers import ImageSerializer
from django.http import FileResponse
from django.conf import settings

import torch
import torchvision.transforms as transforms
import PIL.Image

from SRGANext.utils.origin_module import Generator

import mimetypes
import logging
import os


class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # 保存用户信息
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py
# ...其他导入...

def process_image(image_path):

    save_path = os.path.join('images', 'processed_images', f'{os.path.basename(image_path)}')

    device = torch.device('cpu')

    # 加载预训练的SRGAN模型
    model = Generator()
    # model_dict = torch.load('modules/SRGANext_weight/generator_100.pth')
    model_dict = torch.load('SRGANext/modules/SRGAN_weight/generator_100.pth')
    model.load_state_dict(model_dict)
    model.eval()
    model = model.to(device)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    # 加载测试图像
    img = PIL.Image.open(image_path)

    # 对测试图像进行预处理
    img = transform(img)
    img = img.unsqueeze(0)
    img = img.to(device)

    # 将测试图像输入SRGAN模型进行超分辨率重建
    with torch.no_grad():
        output = model(img)

    # 将输出图像转换为PIL.Image对象并保存
    output = output.squeeze(0).cpu().detach().numpy()
    output = (output + 1) / 2.0 * 255.0
    output = output.clip(0, 255).astype('uint8')
    output = PIL.Image.fromarray(output.transpose(1, 2, 0))
    output.save(save_path)

    return os.path.join('processed_images', f'{os.path.basename(image_path)}')


class ImageProcessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            print(pk)
            image = Image.objects.filter(id=pk).first()
            processed_image_path = process_image(image.original_image.path)
            image.processed_image = processed_image_path
            image.save()
            return Response({
                'message': 'Image processed successfully',
                'processed_image': processed_image_path.replace('\\', '/')

            }, status=status.HTTP_200_OK)
        except Image.DoesNotExist:
            return Response({'message': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)


class DownloadProcessedImageView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            image = Image.objects.get(id=pk)  # 确保用户只能访问自己的图片
            processed_image_path = image.processed_image.path

            # 确定文件的 MIME 类型
            file_type, _ = mimetypes.guess_type(processed_image_path)
            if not file_type:
                file_type = 'application/octet-stream'

            # 使用 FileResponse 返回文件流
            response = FileResponse(open(processed_image_path, 'rb'), content_type=file_type)
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(processed_image_path)}"'
            return response

        except Image.DoesNotExist:
            return Response({'message': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        except FileNotFoundError:
            return Response({'message': 'Processed image file not found'}, status=status.HTTP_404_NOT_FOUND)


class ImageHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        images = Image.objects.filter(user=request.user).order_by('-upload_time')
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


class UpdateCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            image = Image.objects.get(id=pk)  # 确保用户只能访问自己的图片
            image.category = request.data.get('category')
            image.save()
            return Response({
                'message': 'Category updated successfully',
                'category': image.category
            }, status=status.HTTP_200_OK)
        except Image.DoesNotExist:
            return Response({'message': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
