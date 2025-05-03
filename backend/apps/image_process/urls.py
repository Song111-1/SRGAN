from django.urls import path
from .views import ImageUploadView, ImageProcessView, DownloadProcessedImageView, ImageHistoryView, UpdateCategoryView

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('process/<int:pk>/', ImageProcessView.as_view(), name='image-process'),
    path('download/processed/<int:pk>/', DownloadProcessedImageView.as_view(), name='download-processed-image'),
    path('image-history/', ImageHistoryView.as_view(), name='image-history'),
    path('update-category/<int:pk>/', UpdateCategoryView.as_view(), name='update-category'),
    # 其他 URL...
]
