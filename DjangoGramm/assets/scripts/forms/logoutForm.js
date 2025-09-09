import {createApp} from "vue";
import LogoutForm from "../components/LogoutForm.vue";

export function initLogoutForm() {
    const appElement = document.getElementById('logout-app');

    if (!appElement) {
        console.error('Container for form is not found');
        return;
    }

    const app = createApp({
        components: { LogoutForm },
        template: '<LogoutForm/>'
    });

    app.mount(appElement);
}