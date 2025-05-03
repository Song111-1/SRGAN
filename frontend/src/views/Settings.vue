<template>
  <div class="profile-container">
    <div class="user-info">
      <h2>{{ userInfo.username }}</h2>
<!--      <el-input v-else v-model="editUserInfo.username" placeholder="用户名"></el-input>-->

      <div v-if="!isEditing"><strong>名：</strong>{{ userInfo.first_name }}</div>
      <el-input v-else v-model="editUserInfo.first_name" placeholder="名字"></el-input>

      <div v-if="!isEditing"><strong>姓：</strong>{{ userInfo.last_name }}</div>
      <el-input v-else v-model="editUserInfo.last_name" placeholder="姓氏"></el-input>

      <div v-if="!isEditing"><strong>邮箱：</strong>{{ userInfo.email }}</div>
      <el-input v-else v-model="editUserInfo.email" placeholder="邮箱"></el-input>

      <el-button v-if="!isEditing" type="primary" @click="isEditing = true">编辑</el-button>
      <el-button v-else type="success" @click="saveUserInfo">保存</el-button>

      <div v-if="isEditingPassword" style="margin-top: 10px">
        <el-input v-model="editPassword.newPassword" placeholder="新密码" type="password"></el-input>
        <el-input v-model="editPassword.confirmPassword" placeholder="确认新密码" type="password"></el-input>
        <el-button type="success" @click="changePassword">修改密码</el-button>
        <el-button @click="isEditingPassword = false">取消</el-button>
      </div>
      <el-button v-if="!isEditing && !isEditingPassword" type="primary" @click="isEditingPassword = true">修改密码</el-button>

    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue';
import { apiService } from '../utils/apiService';
import { onMounted } from "vue";
import { ElMessage } from 'element-plus';

const userInfo = ref({ username: '', first_name: '', last_name: '', email: '' });
const editUserInfo = ref({ ...userInfo.value });
const isEditing = ref(false);

const getUserInfo = async () => {
  try {
    const userResponse = await apiService.getPrivateData('/auth/user_info/', {});
    if (userResponse.status === 200) {
      Object.assign(userInfo.value, userResponse.data);
      Object.assign(editUserInfo.value, userInfo.value);
      console.log(userInfo.value);
    }
  } catch (error) {
    console.error('获取用户信息失败', error);
  }
};

const saveUserInfo = async () => {
  // 更新用户信息的逻辑
  userInfo.value = { ...editUserInfo.value };
  isEditing.value = false;
  console.log(userInfo.value);
  // 在这里添加调用 API 更新后端数据的代码
  // 例如: await apiService.postPrivateData('/auth/update_user_info/', editUserInfo.value);
  try {
    const userResponse = await apiService.postPrivateData('/auth/user_info/update/', editUserInfo.value);
    if (userResponse.status === 200) {
      Object.assign(userInfo.value, userResponse.data);
      Object.assign(editUserInfo.value, userInfo.value);
      console.log(userInfo.value);
    }
  } catch (error) {
    console.error('获取用户信息失败', error);
  }
};

const isEditingPassword = ref(false);
const editPassword = ref({ newPassword: '', confirmPassword: '' });

const changePassword = async () => {
  if (editPassword.value.newPassword !== editPassword.value.confirmPassword) {
    console.error('密码不匹配');
    ElMessage.error('密码不匹配');
    return;
  }

  if (editPassword.value.newPassword.length < 6) {
    console.error('密码长度不能少于 6 位');
    ElMessage.error('密码长度不能少于 6 位');
    return;
  }


  // 在这里添加密码复杂度检查（可选）

  // 调用API来更新密码
  try {
    const passwordResponse = await apiService.postPrivateData('/auth/change_password/', {
      new_password: editPassword.value.newPassword
    });
    if (passwordResponse.status === 200) {
      console.log('密码修改成功');
      isEditingPassword.value = false;
    }
  } catch (error) {
    console.error('修改密码失败', error);
  }
};

onMounted(() => {
  getUserInfo();
});
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f7f7f7;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.user-info {
  width: 100%;
}

.user-info h2 {
  margin-bottom: 15px;
  color: #333;
  font-size: 2em;
}

.user-info div {
  margin-bottom: 10px;
  color: #555;
  line-height: 1.6;
}

.el-input {
  width: 100%;
  margin-bottom: 10px;
}

.el-button {
  margin-top: 20px;
  border-radius: 4px;
}

.el-button:hover {
  background-color: #409eff;
  color: white;
}

</style>
