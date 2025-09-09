import {createApp} from "vue";
import ProfileEditForm from "../components/ProfileEditForm.vue";

export function initProfileEditForm() {
    const appElement = document.getElementById('edit-profile-app');

    if (!appElement) {
        console.error('Container for form is not found');
        return;
    }

    const app = createApp({
        components: { ProfileEditForm },
        template: '<ProfileEditForm/>'
    });

    app.mount(appElement);
}