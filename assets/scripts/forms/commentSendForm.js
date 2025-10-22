import { createApp } from "vue";
import CommentSendForm from "../components/CommentSendForm.vue";

export function initCommentForm() {
    const appElements = document.querySelectorAll('.comment-container');

    appElements.forEach((element) => {
        const postId = parseInt(element.dataset.postId, 10);
        const isAuthenticated = element.dataset.isAuthenticated === 'true';

        const app = createApp(CommentSendForm, { postId, isAuthenticated })
        app.mount(element);
    })
}