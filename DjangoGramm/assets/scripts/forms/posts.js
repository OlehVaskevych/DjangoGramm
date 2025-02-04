import { createApp } from 'vue';
import post from '../components/post.vue';

export function initPosts() {
    const appElement = document.getElementById('posts-app');

    if (!appElement) {
        console.error('Container for posts is not found');
        return;
    }

    const app = createApp( {
        components: { post },
        template: '<post/>'
    });

    app.mount(appElement);
}
