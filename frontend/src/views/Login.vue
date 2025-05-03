<template>
  <div class="login-container">
      <el-card class="login-card">
      <div class="title-container">
          <h1 class="title">超分像素系统 - 登录</h1>
      </div>
      <el-form :model="loginForm" :rules="rules" @submit.prevent="handleLogin" label-width="80px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="loginForm.username" placeholder="用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="loginForm.password" type="password" placeholder="密码"></el-input>
          </el-form-item>
          <el-form-item label="验证码" prop="captcha">
            <el-input v-model="loginForm.captcha" placeholder="验证码"></el-input>
            <img :src="captchaSrc" @click="fetchCaptcha" alt="验证码" class="captcha-image" />
          </el-form-item>
          <el-button type="primary" block native-type="submit">登录</el-button>
      </el-form>
      <p class="register-invite">
        没有账号？<el-link type="primary" @click="navigateToRegister">立即注册</el-link>
      </p>
      </el-card>
  </div>
  </template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { apiService } from '../utils/apiService';
import { useAuthStore } from '../stores/authStore';
import { ElMessage } from 'element-plus';

const router = useRouter();
const authStore = useAuthStore();

const loginForm = reactive({
  username: '',
  password: '',
  captcha: ''  // 验证码字段
});

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ],
    captcha: [
    { required: true, message: '请输入验证码', trigger: 'blur' }
  ]
};

const captchaSrc = ref('');

const fetchCaptcha = () => {
  captchaSrc.value = '/api/auth/captcha/?rand=' + Math.random();
};

const handleLogin = async () => {
  try {
    const tokenResponse = await apiService.postPublicData('/auth/token/', {
      username: loginForm.username,
      password: loginForm.password,
      captcha: loginForm.captcha  // 将验证码字段传递给后端
    });

    if (tokenResponse.status === 200) {
      const { access, refresh } = tokenResponse.data;

      // 更新 Pinia store 中的令牌信息
      authStore.setTokens(access, refresh);

      // 获取用户信息
      try {
        const userResponse = await apiService.getPrivateData('/auth/user_info/', {});
        if (userResponse.status === 200) {
          const userInfo = userResponse.data;
          authStore.login({ name: userInfo.username, access, refresh });  // 假设用户名字段为 'username'
          ElMessage.success('登录成功');
          router.push('/'); // 导航到首页
        }
      } catch (userErr) {
        ElMessage.error(userErr.response.data.error);
      }

    }
  } catch (err) {
    ElMessage.error(err.response.data.error);
  }
};


const navigateToRegister = () => {
  router.push('/register'); // 导航到注册页面
};

onMounted(() => {
  fetchCaptcha();
});
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #4A90E2;
}

.login-card {
  width: 400px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.title-container {
  text-align: center;
  margin-bottom: 20px;
}

.title {
  color: #2c3e50;
  font-weight: bold;
}

.el-form-item {
  margin-bottom: 15px;
}

.register-invite {
  text-align: left;
  margin-top: 15px;
}

.captcha-image {
  cursor: pointer;
  width: 80px;
  height: 30px;
}
</style>
