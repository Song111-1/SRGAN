import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  // 初始化状态
  state: () => ({
    isLogin: JSON.parse(localStorage.getItem('isLogin')) || false,
    user: JSON.parse(localStorage.getItem('user')) || { name: null },
    token: {
      access: localStorage.getItem('accessToken') || null,
      refresh: localStorage.getItem('refreshToken') || null
    }
  }),
  actions: {
    setTokens(access, refresh) {
      this.token.access = access;
      this.token.refresh = refresh;
      // 保存到本地存储
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
    },
    login(user) {
      this.isLogin = true;
      this.user.name = user.name;
      this.setTokens(user.access, user.refresh);
      // 保存登录状态和用户信息
      localStorage.setItem('isLogin', JSON.stringify(true));
      localStorage.setItem('user', JSON.stringify({ name: user.name }));
    },
    logout() {
      this.isLogin = false;
      this.user.name = null;
      this.token.access = null;
      this.token.refresh = null;
      // 清除本地存储
      localStorage.removeItem('isLogin');
      localStorage.removeItem('user');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    }
  }
});
