import { createRouter, createWebHistory } from 'vue-router';

import HomePage from './pages/HomePage.vue';
import LoginPage from './pages/LoginPage.vue';
import RegisterPage from './pages/RegisterPage.vue';
import ProfilePage from './pages/ProfilePage.vue';
import PostPage from './pages/PostPage.vue';
import PostCreationPage from './pages/PostCreationPage.vue';
import SettingsPage from "./pages/SettingsPage.vue";
import PostEditPage from "./pages/PostEditPage.vue";

const routes = [
    { path: '/', component: HomePage },
    { path: '/auth/login', component: LoginPage },
    { path: '/auth/register', component: RegisterPage },
    { path: '/profile/:username', component: ProfilePage },
    { path: '/posts/:id', component: PostPage },
    { path: '/post/', component: PostCreationPage },
    { path: '/settings/', component: SettingsPage },
    { path: '/post/:id/update', component: PostEditPage },
]

export default createRouter({
    history: createWebHistory(),
    routes,
});