import { createApp } from "vue";
import CommentDeleteForm from "../components/CommentDeleteForm.vue";

export function initCommentDeleteForm() {
    const appElements = document.querySelectorAll('.comment-delete-container');

    appElements.forEach((element) => {
        const postId = parseInt(element.dataset.postId, 10);
        const commentId = parseInt(element.dataset.commentId, 10);

        const app = createApp(CommentDeleteForm, { postId, commentId });
        app.mount(element);
    })
}