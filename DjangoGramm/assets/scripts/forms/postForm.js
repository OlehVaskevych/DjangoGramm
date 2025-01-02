import { createApp } from 'vue';
import PostForm from '../components/PostForm.vue';

export function initPostForm() {
    // Знайти контейнер для рендерингу
    const appElement = document.getElementById('create-post-app');

    const app = createApp({
        components: { PostForm },
        data() {
            return {
                formFields: [
                    {
                        id: 'title',
                        label: 'Title',
                        value: '',
                        attrs: { type: 'text', name: 'title', required: true },
                        helpText: 'Enter the title of your post',
                        errors: [],
                    },
                    {
                        id: 'description',
                        label: 'Description',
                        value: '',
                        attrs: { type: 'text', name: 'description', required: true },
                        helpText: 'Enter a short description',
                        errors: [],
                    },
                ],
            };
        },
        template: `<PostForm :fields="formFields" />`,
    });

    app.mount(appElement);

    if (!appElement) {
        console.error('Контейнер #create-post-app не знайдено');
    }
}
