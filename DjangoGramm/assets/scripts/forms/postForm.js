import { createApp } from 'vue';
import PostForm from '../components/PostForm.vue';

export function initPostForm() {
    // Знаходимо контейнер для рендерингу
    const appElement = document.getElementById('create-post-app');

    if (!appElement) {
        console.error('Container for form is not found.');
        return;
    }

    // Ініціалізуємо Vue-додаток із компонентом PostForm
    const app = createApp({
        components: { PostForm },
        data() {
            return {
                fields: [
                    {
                        id: 'title',
                        label: 'Title',
                        value: '',
                        type: 'text',
                        name: 'title',
                        required: true,
                        errors: []
                    },
                    {
                        id: 'description',
                        label: 'Description',
                        value: '',
                        type: 'text',
                        name: 'description',
                        required: true,
                        errors: []
                    },
                ],
            };
        },
        template: '<PostForm :form-model="{ fields }" />',
    });

    app.mount(appElement);
}
