import { createApp } from "vue";
import LikeAddForm from "../components/LikeAddForm.vue";

export function initLikeForm() {
    const appElements = document.querySelectorAll('.like-container')

    if (appElements.length === 0) {
        console.error("No like containers found");
        return;
    }

    appElements.forEach((element) => {
        const postId = parseInt(element.dataset.postId, 10);
        const isLiked = element.dataset.isLiked === 'true';

        const app = createApp(LikeAddForm, { postId, isLiked });
        app.mount(element);
    });
}
