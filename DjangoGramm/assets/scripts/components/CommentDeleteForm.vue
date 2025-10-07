<template>
  <form @submit.prevent="submitForm" enctype="multipart/form-data" class="d-inline">
    <button type="submit" class="btn btn-danger btn-sm"><i style="font-size:24px" class="fa-solid fa-trash"></i></button>
  </form>
</template>

<script>
import { getCookie } from "../csrf.js";

export default {
  props: {
    postId: {
      type: Number,
      required: true,
    },
    commentId: {
      type: Number,
      required: true,
    }
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch(`/post/${this.postId}/comments/${this.commentId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
          },
        });

        const data = await response.json();

        if (response.ok) {
          this.$emit('delete-comment', data);
        } else {
          console.error('Failed to delete comment');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
};
</script>