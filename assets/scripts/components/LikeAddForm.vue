<template>
  <button @click="toggleLike" class="custom-btn-like">
    <i :class="heartIconClass" style="font-size:24px"></i>
  </button>
</template>

<script>
import { getCookie } from '../csrf.js';

export default {
  props: {
    postId: Number,
    isLiked: Boolean,
    likesCount: Number,
  },
  data() {
    return {
      liked: this.isLiked,
      likes: this.likesCount,
    };
  },
  computed: {
    heartIconClass() {
      return this.liked ? "fa-solid fa-heart" : "fa-regular fa-heart";
    },
  },
  methods: {
    async toggleLike() {
      try {
        const response = await fetch(`/api/post/${this.postId}/likes`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
          },
          credentials: "include",
        });

        const { data } = await response.json();

        if (response.ok) {
          this.liked = !this.liked;
          this.$emit("like-updated", data.likes_count);
        } else {
          console.error("Failed to update like status");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
  },
};
</script>
