<template>
  <div class="favorites-container">
    <div v-for="(items, category) in categorizedImages" :key="category">
      <h2>{{ category }}</h2>
      <hr />
      <el-row :gutter="20">
        <el-col :span="24" :md="12" :lg="8" :xl="6" v-for="item in items" :key="item.id">
          <el-card class="image-card">
            <div style="display: flex;">
              <img :src="item.original_image" alt="原图" class="image-preview"/>
              <div class="card-content">
                <p>类别: {{ item.category }}</p>
                <div class="button-group">
                  <el-button size="default" @click="downloadImage(item.original_image)">下载原始图</el-button>
                  <el-button size="default" @click="downloadImage(item.processed_image)">下载处理图</el-button>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { apiService } from '../utils/apiService';

const imageHistory = ref([]);
const categorizedImages = ref({});

const downloadImage = (url) => {
  const link = document.createElement('a');
  link.href = url;
  link.download = url.split('/').pop();
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const categorizeImages = () => {
  categorizedImages.value = imageHistory.value.reduce((acc, img) => {
    if (!acc[img.category]) {
      acc[img.category] = [];
    }
    acc[img.category].push(img);
    return acc;
  }, {});
};

onMounted(async () => {
  try {
    const response = await apiService.getPrivateData('/image/image-history/', {});
    imageHistory.value = response.data.map(item => ({
      ...item,
      original_image: '/api' + item.original_image,
      processed_image: '/api' + item.processed_image
    }));
    categorizeImages();
  } catch (error) {
    console.error('Error fetching image history:', error);
  }
});
</script>

<style scoped>
.favorites-container {
  padding: 20px;
}

.image-card {
  width: 300px; /* 设置固定宽度 */
  box-sizing: border-box; /* 确保边框和内边距不会使元素超出设定宽度 */
  margin-bottom: 20px;
}

.card-content {
  flex-grow: 1;
  margin-left: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.button-group {
  display: flex;
  flex-direction: column;
  align-items: stretch; /* 使按钮在水平方向上拉伸填满容器 */
}

.el-button {
  margin-bottom: 10px; /* 为按钮之间添加间隔 */
  margin-left: 0;
}


.image-preview {
  width: 100px;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
}

hr {
  margin: 10px 0;
}

.el-col {
  display: flex;
  justify-content: center;
}
</style>
