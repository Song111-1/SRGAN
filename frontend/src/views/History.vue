<template>
  <div class="image-history-container">
    <el-table :data="imageHistory" style="width: 100%" stripe>
      <el-table-column prop="upload_time" label="上传时间" width="180" :formatter="formatDate"></el-table-column>
      <el-table-column label="分类" width="180">
        <template #default="scope">
          <div v-if="!scope.row.editing" class="category-text">{{ scope.row.category }}</div>
          <el-input v-else v-model="scope.row.editingCategory" size="mini" class="category-input"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="图片">
        <template #default="scope">
          <img :src="scope.row.original_image" alt="原图" class="image-preview"/>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button v-if="!scope.row.editing" size="mini" @click="editCategory(scope.row)">编辑</el-button>
          <el-button v-else size="mini" type="primary" @click="saveCategory(scope.row)">保存</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { apiService } from '../utils/apiService';
import moment from 'moment';

const imageHistory = ref([]);

const editCategory = (row) => {
  row.editing = true;
  row.editingCategory = row.category;
};

const saveCategory = async (row) => {
  try {
    const response = await apiService.postPrivateData(`/image/update-category/${row.id}/`, { category: row.editingCategory });
    if (response.status === 200) {
      row.category = row.editingCategory;
    }
  } catch (error) {
    console.error('Error saving category:', error);
  }
  row.editing = false;
};

const formatDate = (row, column, cellValue) => {
  return moment(cellValue).format('YYYY-MM-DD HH:mm:ss');
};

onMounted(async () => {
  try {
    const response = await apiService.getPrivateData('/image/image-history/', {});
    imageHistory.value = response.data.map(item => ({
      ...item,
      original_image: '/api' + item.original_image,
      editing: false
    }));
  } catch (error) {
    console.error('Error fetching image history:', error);
  }
});
</script>

<style scoped>
.image-history-container {
  padding: 20px;
  background: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.category-text {
  font-size: 14px;
}

.category-input {
  max-width: 160px;
}

.image-preview {
  width: 100px;
  height: auto;
  margin-right: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
