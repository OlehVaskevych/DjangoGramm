import { createRouter, createWebHistory } from 'vue-router';
import { getCookie } from './csrf.js';

import HomePage from './pages/HomePage.vue';
import LoginPage from './pages/LoginPage.vue';
import RegisterPage from './pages/RegisterPage.vue';
import ProfilePage from './pages/ProfilePage.vue';
import PostPage from './pages/PostPage.vue';
import PostCreationPage from './pages/PostCreationPage.vue';
import SettingsPage from './pages/SettingsPage.vue';
import PostEditPage from './pages/PostEditPage.vue';
import ProfileEditPage from "./pages/ProfileEditPage.vue";

const routes = [
  { path: '/', component: HomePage },
  { path: '/auth/login', component: LoginPage },
  { path: '/auth/register', component: RegisterPage },
  { path: '/auth/logout',
    name: 'logout',
    beforeEnter: async (to, from, next) => {
      try {
        await fetch('/auth/logout/', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
          },
        });
        window.currentUser = null;
        window.userIsAuthenticated = false;

        localStorage.removeItem('authUser');
      } catch (err) {
        console.warn('Logout failed:', err);
      }
      window.location.href = "/";
    },
  },

  { path: '/profile/:username', component: ProfilePage },
  { path: '/posts/:id', component: PostPage },
  { path: '/post/', component: PostCreationPage },
  { path: '/settings/', component: SettingsPage },
  { path: '/post/:id/update', component: PostEditPage },
  { path: '/profile/:username/update', component: ProfileEditPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

console.log('✅ Routes:', router.getRoutes().map(r => r.path));

export default router;
