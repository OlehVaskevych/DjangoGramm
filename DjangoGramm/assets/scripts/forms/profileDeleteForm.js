import {createApp} from "vue";
import ProfileDeleteForm from "../components/ProfileDeleteForm.vue";

export function initProfileDeleteForm() {
    const appElement = document.getElementById('delete-profile-app');

    if(!appElement) {
        console.error('Container for form is not found');
        return;
    }
    const app = createApp({
        components: { ProfileDeleteForm },
        template: '<ProfileDeleteForm/>'
    });

    app.mount(appElement);
}