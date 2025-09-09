import 'bootstrap'; // Імпорт Bootstrap JS
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/styles.css'; // Імпорт вашого CSS
import { initNavigation } from './navigation/navigation';
import { initPostForm } from './forms/postForm';
import { initPostEditForm } from "./forms/postEditForm";
import { initPostDeleteForm } from "./forms/postDeleteForm";
import { initProfileEditForm } from "./forms/profileEditForm";
import { initProfileDeleteForm } from "./forms/profileDeleteForm";
import { initRegisterForm } from "./forms/registerForm";
import { initLoginForm } from "./forms/loginForm";
import { initLogoutForm } from "./forms/logoutForm";
import { initPosts } from "./forms/posts";

document.addEventListener('DOMContentLoaded', () => {
    // Ініціалізуємо форму, якщо вона є на сторінці
    const postFormContainer = document.getElementById('create-post-app');
    const postEditFormContainer = document.getElementById('edit-post-app');
    const postDeleteFormContainer = document.getElementById('delete-post-app');
    const profileEditFormContainer = document.getElementById('edit-profile-app');
    const profileDeleteFormContainer = document.getElementById('delete-profile-app');
    const registerFormContainer = document.getElementById('register-app');
    const loginFormContainer = document.getElementById('login-app');
    const logoutFormContainer = document.getElementById('logout-app');
    const postsContainer = document.getElementById('posts-app');

    if (postsContainer) {
        initPosts();
    }

    if (postFormContainer) {
        initPostForm();
    }

    if (postEditFormContainer) {
        initPostEditForm();
    }

    if (postDeleteFormContainer) {
        initPostDeleteForm();
    }

    if (profileEditFormContainer) {
        initProfileEditForm();
    }

    if (profileDeleteFormContainer) {
        initProfileDeleteForm();
    }

    if (registerFormContainer) {
        initRegisterForm();
    }

    if (loginFormContainer) {
        initLoginForm();
    }

    if (logoutFormContainer) {
        initLogoutForm();
    }

    // Ініціалізуємо навігацію
    initNavigation();
});
