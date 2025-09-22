import { createRouter, createWebHistory } from 'vue-router';

import HomePage from './pages/HomePage.vue';
import LoginPage from './pages/LoginPage.vue';
import RegisterPage from './pages/RegisterPage.vue';
import ProfilePage from './pages/ProfilePage.vue';
import PostPage from './pages/PostPage.vue';

const routes = [
    { path: '/', component: HomePage },
    { path: '/auth/login', component: LoginPage },
    { path: '/auth/register', component: RegisterPage },
    { path: '/profile/:id', component: ProfilePage },
    { path: '/post/:id', component: PostPage },
]

export default createRouter({
    history: createWebHistory(),
    routes,
});