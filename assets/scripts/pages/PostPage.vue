<template>
  <div v-if="post">
    <PostDetail
      :post="post"
      :currentUser="currentUser"
      :userIsAuthenticated="userIsAuthenticated"
      @update-post="handlePostUpdate"
      @update-post-comments="handleCommentsUpdate"
    />
  </div>
  <div v-else class="alert alert-warning text-center">Post not found.</div>
</template>

<script>
import PostDetail from '../components/PostDetail.vue';
import LikeAddForm from '../components/LikeAddForm.vue';
import CommentSendForm from "../components/CommentSendForm.vue";
import CommentDeleteForm from "../components/CommentDeleteForm.vue";

export default {
  // 3. Реєструємо PostDetail
  components: { PostDetail, LikeAddForm, CommentSendForm, CommentDeleteForm },
  data() {
    return {
      post: null,
      currentUser: null,
      userIsAuthenticated: false
    };
  },
  methods: {
    // Ці методи обробляють події від PostDetail і мутують this.post
    handlePostUpdate(update) {
      // Оновлюємо кількість лайків безпосередньо в this.post
      if (this.post && update.field === 'likes.count') {
        this.post.likes.count = update.value;
      }
    },
    handleCommentsUpdate(update) {
      if (!this.post) return;

      if (update.action === 'send') {
        // Додавання нового коментаря
        this.post.comments.push(update.comment);
      } else if (update.action === 'delete') {
        // Видалення коментаря
        const index = this.post.comments.findIndex(c => c.id === update.comment.id);
        if (index !== -1) {
          this.post.comments.splice(index, 1);
        }
      }
    }
  },
  async mounted() {
    // Логіка завантаження поста залишається без змін
    try {
      const postId = this.$route.params.id;
      const res = await fetch(`/api/post/${postId}/`);
      const { data } = await res.json();
      this.post = data.post;
      this.currentUser = data.currentUser;
      this.userIsAuthenticated = data.userIsAuthenticated;
    } catch (err) {
      console.error('Failed to load post:', err);
      this.post = false; // Встановлюємо false, щоб показати "Post not found"
    }
  }
};
</script>