import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/authStore.js";

const routes = [
  {
    path: '/',
    redirect: '/home',
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../components/Layout.vue'),
    children: [
      {
        path: '/home',
        name: 'Home',
        component: () => import('../views/Home.vue'),
      },
    ],
    meta: { requiresAuth: true } // 标记需要认证的路由
  },
  {
    path: '/setting',
    name: 'Settings',
    component: () => import('../components/Layout.vue'),
    children: [
      {
        path: '/setting',
        name: 'Settings',
        component: () => import('../views/Settings.vue'),
      },
    ],
    meta: { requiresAuth: true } // 标记需要认证的路由
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../components/Layout.vue'),
    children: [
      {
        path: '/history',
        name: 'History',
        component: () => import('../views/History.vue'),
      },
    ],
    meta: { requiresAuth: true } // 标记需要认证的路由
  },
  {
    path: '/collect',
    name: 'Collect',
    component: () => import('../components/Layout.vue'),
    children: [
      {
        path: '/collect',
        name: 'Collect',
        component: () => import('../views/Collect.vue'),
      },
    ],
    meta: { requiresAuth: true } // 标记需要认证的路由
  },
];


const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore(); // 获取认证状态
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !authStore.isLogin) {
    // 如果需要认证，但用户未登录，重定向到登录页面
    next({ name: 'Login' });
  } else {
    // 否则，正常导航
    next();
  }
});

export default router;
