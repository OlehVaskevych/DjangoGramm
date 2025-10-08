import { createApp } from 'vue';
import App from './App.vue';
import 'bootstrap'; // Імпорт Bootstrap JS
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/styles.scss'; // Імпорт вашого CSS
import router from './router';

const el = document.getElementById('app')

const app = createApp(App, {
    isAuthenticated: el.dataset.auth === "true",
    currentPath: el.dataset.path,
    username: el.dataset.username || "",
})

app.use(router);
app.mount("#app");

// createApp(App).use(router).mount('#app');