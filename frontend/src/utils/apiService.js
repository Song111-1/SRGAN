import axios from 'axios';
import { useAuthStore } from '../stores/authStore'; // 确保路径正确

const API_BASE_URL = 'http://www.ryanstone.cn:5173/api/';

const apiInstance = axios.create({
  baseURL: API_BASE_URL
});

const authApiInstance = axios.create({
  baseURL: API_BASE_URL
});

const authStore = useAuthStore();

authApiInstance.interceptors.request.use(config => {
  const { access } = authStore.token;
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

authApiInstance.interceptors.response.use(response => {
  return response;
}, async error => {
  const originalRequest = error.config;
  if (error.response.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true;
    try {
      // 使用刷新令牌获取新令牌
      const { refresh } = authStore.token;
      const response = await apiInstance.post('/auth/token/refresh/', { refresh });
      const { access, refresh: newRefresh } = response.data;

      // 更新存储的令牌
      authStore.setTokens(access, newRefresh);

      // 更新原请求的令牌并重试
      originalRequest.headers.Authorization = `Bearer ${access}`;
      return authApiInstance(originalRequest);
    } catch (refreshError) {
      // 处理刷新令牌失败
      return Promise.reject(refreshError);
    }
  }
  return Promise.reject(error);
});

export const apiService = {
  // 无需验证的 API 请求
  getPublicData(url, params) {
    return apiInstance.get(url, { params });
  },

  // 需要验证的 API 请求
  getPrivateData(url, params) {
    return authApiInstance.get(url, { params });
  },

  postPublicData(url, data) {
    return apiInstance.post(url, data);
  },

  postPrivateData(url, data) {
    return authApiInstance.post(url, data);
  },
};
