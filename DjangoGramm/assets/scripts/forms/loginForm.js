import {createApp} from "vue";
import LoginForm from "../components/LoginForm.vue";

export function initLoginForm() {
    const appElement = document.getElementById('login-app');

    if (!appElement) {
        console.error('Container for form is not found');
        return;
    }

    const app = createApp({
        components: { LoginForm },
        template: '<LoginForm/>'
    });

    app.mount(appElement);
}