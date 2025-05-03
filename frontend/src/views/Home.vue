<template>
  <div class="home-container">
    <div v-if="!isLogin" class="login-prompt">请登录</div>
    <div v-else class="image-container">
      <div v-if="!imageSrc" class="upload-box">
        <input type="file" @change="onFileChange" hidden ref="fileInput" />
        <el-button type="primary" @click="triggerFileInput">上传图片</el-button>
      </div>

      <img v-if="imageSrc && !processedImageSrc" :src="imageSrc" class="uploaded-image" />

      <div v-if="processedImageSrc" class="processed-image-box">
        <img :src="processedImageSrc" class="processed-image" />
        <el-button type="info" @click="downloadImage">下载图片</el-button>
      </div>

      <el-button v-if="imageSrc && !processedImageSrc" type="success" @click="processImage">处理图片</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/authStore';
import { apiService } from '../utils/apiService';
import {ElMessage} from "element-plus";

const authStore = useAuthStore();
const isLogin = authStore.isLogin;
const imageSrc = ref(null); // 上传的图片 URL
const imageId = ref(null); // 上传的图片 ID
const processedImageSrc = ref(false); // 处理后的图片 URL
const fileInput = ref(null);

const triggerFileInput = () => {
  console.log(fileInput);
  if (fileInput.value) {
    fileInput.value.click();
  }
};

const onFileChange = async (event) => {
  const file = event.target.files[0];
  if (file) {
    // 显示图片预览
    const reader = new FileReader();
    reader.onload = (e) => {
      imageSrc.value = e.target.result;
    };
    reader.readAsDataURL(file);

    // 调用上传接口
    try {
      const formData = new FormData();
      formData.append('original_image', file);
      const response = await apiService.postPrivateData('/image/upload/', formData);
      if (response.status === 201) {
        const { id } = response.data;
        imageId.value = id;
      }
    } catch (error) {
      console.error('图片上传失败', error);
    }
  }
};

const processImage = async () => {
  try {
    const response = await apiService.getPrivateData('/image/process/' + imageId.value + '/', {});
    if (response.status === 200) {
      const { processed_image } = response.data;
      processedImageSrc.value = '/api/images/' + processed_image;
      console.log(processedImageSrc.value)
      ElMessage.success('图片处理成功');
    }
  } catch (error) {
    console.error('处理图片失败', error)
  }
};

const downloadImage = () => {
  const link = document.createElement('a');
  link.href = processedImageSrc.value;
  link.download = 'processed-image'; // 你可以给文件命名或者使用 imageId 来命名文件
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

</script>

<style scoped>
.home-container {
  text-align: center;
  padding: 20px;
}

.login-prompt {
  font-size: 20px;
  color: #333;
}

.image-container {
  width: 100%;
  max-width: 800px; /* 增大最大宽度 */
  margin: 20px auto; /* 调整外边距 */
}

.upload-box {
  border: 2px dashed #d3d3d3;
  padding: 40px; /* 增大内边距 */
  cursor: pointer;
  height: 400px; /* 设置高度 */
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.uploaded-image, .processed-image {
  max-width: 100%;
  max-height: 400px; /* 设置最大高度 */
  display: block;
  margin: 10px auto;
}

.processed-image-box {
  position: relative;
  display: inline-block;
}

.el-button {
  margin: 10px 0;
}
</style>

