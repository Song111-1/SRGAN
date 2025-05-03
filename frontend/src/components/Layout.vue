<template>
  <el-container style="height: 100vh; display: flex; flex-direction: column;">
    <el-header class="header">
      <div class="header-title">
        <h1>超分像素系统</h1>
      </div>

      <div class="header-userinfo">
        <!-- 条件渲染：如果已登录，则显示用户信息和下拉菜单 -->
        <el-dropdown v-if="isLoggedIn">
          <span class="el-dropdown-link">
            <span>欢迎您, {{ loginedUser.username }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="toSettings">个人中心</el-dropdown-item>
              <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <!-- 如果未登录，显示登录按钮 -->
        <el-button v-else type="primary" @click="login">登录</el-button>
      </div>
    </el-header>

    <el-container style="height: 100vh">
      <el-aside width="200px">
        <el-menu
          :default-active="activeIndex.value"
          class="el-menu-vertical-demo"
          @select="handleSelect"
        >
        <el-menu-item index="1">
          <el-icon><Clock /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="2" >
          <el-icon><document /></el-icon>
          <span>历史记录</span>
        </el-menu-item>
        <el-menu-item index="3" >
          <el-icon><document /></el-icon>
          <span>收藏夹</span>
        </el-menu-item>
        <el-menu-item index="4">
          <el-icon><setting /></el-icon>
          <span>个人设置</span>
        </el-menu-item>
      </el-menu>
      </el-aside>

      <el-main>
        <router-view :key="$route.fullPath"></router-view>
      </el-main>

    </el-container>
  </el-container>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';
import {useRouter} from "vue-router";
import { useAuthStore } from "../stores/authStore.js";

const userStore = useAuthStore();

const isLoggedIn = userStore.isLogin
const loginedUser = reactive({
  username: userStore.user.name
});

const activeIndex = ref('1');

const router = useRouter();
// 登录逻辑
const login = () => {
  // 跳转到登录页
  console.log('login');
  router.push('/login');
};

// 退出登录逻辑
const logout = () => {
  userStore.logout()
  // 刷新当前页面
  router.go(0);
};


const handleSelect = (key) => {
  if (key === '1') {
    router.push('/');
  } else if (key === '2') {
    router.push('/history');
  } else if (key === '4') {
    router.push('/setting');
  } else if (key === '3') {
    router.push('/collect');
  }
};

const toSettings = () => {
  router.push('/setting');
};

watch(() => router.currentRoute.value, (newRoute) => {
  activeIndex.value = newRoute.path;
});
</script>


<style lang="less" scoped>
@primary-color: #4A90E2; // 主题色
@text-color: #333; // 文本色
@font-family: 'Helvetica Neue', Arial, sans-serif; // 字体


.el-container {
  height: 100vh;

  .el-aside {
    height: 100%;
    background-color: #f0f0f0; // 可根据需要调整背景色
    border-right: 1px solid @primary-color;
    text-align: center;
  }

  // 其他样式...
}

.header {
  background-color: @primary-color;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  .header-title {
    h1 {
      color: white;
      font-family: @font-family;
      margin: 0;
    }
  }
  .header-userinfo {
    display: flex;
    align-items: center;
    .el-dropdown-link {
      color: white;
      display: flex;
      align-items: center;
      img {
        border-radius: 50%;
        margin-right: 5px;
        width: 40px;
        height: 40px;
      }
      span {
        color: white;
        margin-left: 5px;
      }
    }
  }
}

.el-button {
  border: none;
  background-color: lighten(@primary-color, 10%);
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s, box-shadow 0.3s;

  &:hover {
    background-color: darken(@primary-color, 10%);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    .header-userinfo {
      margin-top: 10px;
    }
  }
}

.el-menu {
  background-color: #fff; // 根据需要调整背景色
  border-right: 1px solid @primary-color;
  text-align: center;

  .el-menu-item {
    color: @text-color;
    &:hover {
      background-color: lighten(@primary-color, 10%); // 鼠标悬停背景色
      color: white; // 鼠标悬停文字色
    }
  }
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  .el-menu-item {
    border-radius: 4px; // 菜单项圆角
    margin: 5px 0; // 调整间距
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); // 添加阴影
  }
}

</style>


