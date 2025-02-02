import {createApp} from "vue";
import PostDeleteForm from "../components/PostDeleteForm.vue";

export function initPostDeleteForm() {
    const appElement = document.getElementById('delete-post-app');

    if (!appElement) {
        console.error('Container for form is not found');
        return;
    }
    const app = createApp({
        components: { PostDeleteForm },
        template: '<PostDeleteForm/>'
    });

    app.mount(appElement);
}