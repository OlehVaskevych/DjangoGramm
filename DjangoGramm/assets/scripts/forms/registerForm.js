import {createApp} from "vue";
import RegisterForm from "../components/RegisterForm.vue";

export function initRegisterForm() {
    const appElement = document.getElementById('register-app');

    if (!appElement) {
        console.error('Container for form is not found');
        return;
    }

    const app = createApp({
        components: { RegisterForm },
        template: '<RegisterForm/>'
    });

    app.mount(appElement);
}