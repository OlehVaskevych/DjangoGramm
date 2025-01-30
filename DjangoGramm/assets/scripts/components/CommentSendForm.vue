<template>
  <form @submit.prevent="submitForm" enctype="multipart/form-data" class="mt-3">
    <textarea v-model="comment" class="form-control mb-2 comment-text custom-text-area" placeholder="Додайте коментар..." required></textarea>
    <button v-if="authenticated" type="submit" class="btn custom-comment-button" :disabled="isSubmitting">Відправити</button>
    <a v-else href="/auth/login/" class="custom-submit-button btn btn-sm">Відправити</a>
  </form>
</template>

<script>
export default {
  props: {
    postId: {
      type: Number,
      required: true
    },
    isAuthenticated: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      comment: '',
      authenticated: this.isAuthenticated,
      isSubmitting: false
    };
  },
  methods: {
    async submitForm() {
      if (this.comment.trim() === '') {
        return;
      }

      this.isSubmitting = true;

      const formData = new FormData();
      formData.append('comment', this.comment);

      try {
        const response = await fetch(`/post/${this.postId}/comments`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: formData,
        });

        const data = await response.json();

        if (response.ok) {
          window.location.reload();
        } else {
          console.error("Failed to send comment");
        }
      } catch (error) {
        this.isSubmitting = false;
        console.error('Error:', error);
      }
    },

    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach((cookie) => {
          cookie = cookie.trim();
          if (cookie.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(cookie.split("=")[1]);
          }
        });
      }
      return cookieValue;
    },
  }
};
</script>