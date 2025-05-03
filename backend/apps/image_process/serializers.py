from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'user', 'upload_time', 'category', 'original_image', 'processed_image']
        read_only_fields = ['user', 'upload_time', 'processed_image']
