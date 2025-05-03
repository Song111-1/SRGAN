<template>
<div class="register-container">
    <el-card class="register-card">
    <div class="title-container">
        <h1 class="title">超分像素系统 - 注册</h1>
    </div>
    <el-form :model="registerForm" :rules="rules" @submit.prevent="handleRegister" label-width="80px">
        <el-form-item label="用户名" prop="username">
        <el-input v-model="registerForm.username" placeholder="用户名" prefix-icon="el-icon-user-solid"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
        <el-input v-model="registerForm.password" type="password" placeholder="密码" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
        <el-input v-model="registerForm.confirmPassword" type="password" placeholder="确认密码" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="captcha">
          <el-input v-model="registerForm.captcha" placeholder="验证码"></el-input>
          <img :src="captchaSrc" @click="fetchCaptcha" alt="验证码" class="captcha-image" />
        </el-form-item>
        <el-button type="primary" block native-type="submit">注册</el-button>
    </el-form>
    <p class="register-invite">
      已有账号？<el-link type="primary" @click="navigateToLogin">点击登录</el-link>
    </p>
    </el-card>
</div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { apiService } from '../utils/apiService';
import { ElMessage } from 'element-plus';

const router = useRouter();
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  captcha: ''  // 验证码字段
});

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'));
        } else {
          callback();
        }
      },
      trigger: 'blur'
    }
  ],
  captcha: [
    { required: true, message: '请输入验证码', trigger: 'blur' }
  ]
};

const captchaSrc = ref('');

const fetchCaptcha = () => {
  captchaSrc.value = '/api/auth/captcha/?rand=' + Math.random();
}

const handleRegister = async () => {
  const submitRegisterForm = {
    username: registerForm.username,
    password: registerForm.password,
    captcha: registerForm.captcha
  };

  try {
    const res = await apiService.postPublicData('/auth/register/', submitRegisterForm);
    console.log(res);

    if (res.status === 201) {
      ElMessage.success('注册成功');
      router.push('/login'); // 注册成功，跳转到登录页面
    }
  } catch (error) {
    console.error('注册失败:', error);
    ElMessage.error('注册失败');
  }
};


const navigateToLogin = () => {
  router.push('/login'); // 导航到登录页面
};

onMounted(() => {
  fetchCaptcha();
});
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #4A90E2;
}

.register-card {
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
</style>
