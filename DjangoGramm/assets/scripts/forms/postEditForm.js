import {createApp} from "vue";
import PostEditForm from '../components/PostEditForm.vue';

export function initPostEditForm() {
    const appElement = document.getElementById('edit-post-app');

    if (!appElement) {
        console.error('Container for form is not found');
        return;
    }
    const app = createApp({
        components: { PostEditForm },
        data() {
            return {
                fields: [
                    {
                        id: 'title',
                        label: 'Title',
                        value: initialData.title,
                        type: 'text',
                        name: 'title',
                        required: false,
                        errors: []
                    },
                    {
                        id: 'description',
                        label: 'Description',
                        value: initialData.description,
                        type: 'text',
                        name: 'description',
                        required: false,
                        errors: []
                    }
                ],
            };
        },
        template: '<PostEditForm :form-model="{ fields }" />'
    });

    app.mount(appElement);
}