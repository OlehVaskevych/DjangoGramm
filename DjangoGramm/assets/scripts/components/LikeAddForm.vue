<template>
  <button @click="toggleLike" class="custom-btn-like">
    <i :class="heartIconClass" style="font-size:24px"></i>
  </button>
</template>

<script>
export default {
  props: {
    postId: Number,
    isLiked: Boolean,
  },
  data() {
    return {
      liked: this.isLiked,
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
        const response = await fetch(`/post/${this.postId}/likes`, {
          method: "POST",
          headers: {
            "X-CSRFToken": this.getCookie("csrftoken"),
            "Content-Type": "application/json",
          },
          credentials: "include",
        });

        const data = await response.json();

        if (response.ok) {
          this.liked = !this.liked;
          window.location.reload();
        } else {
          console.error("Failed to update like status");
        }
      } catch (error) {
        console.error("Error:", error);
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
  },
};
</script>
