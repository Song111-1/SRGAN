from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import os


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, default='none')
    original_image = models.ImageField(upload_to='original_images/')
    processed_image = models.ImageField(upload_to='processed_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username + " - " + self.category

    def save(self, *args, **kwargs):
        creating = not self.pk  # 检查这是否是新记录
        super().save(*args, **kwargs)  # 保存模型

        if creating:
            self.rename_image_file()  # 重命名文件仅在创建新记录时进行

        super().save(update_fields=['original_image'])  # 更新原始图像字段

    def rename_image_file(self):
        if self.original_image:
            ext = os.path.splitext(self.original_image.name)[1]  # 获取文件扩展名
            new_image_name = f'{self.id}{ext}'  # 只设置文件名，不包括路径

            if os.path.basename(self.original_image.name) != new_image_name:
                content = ContentFile(self.original_image.read())
                self.original_image.save(new_image_name, content, save=False)


