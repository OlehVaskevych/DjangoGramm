<template>
  <form @submit.prevent="submitForm" enctype="multipart/form-data" class="d-inline">
    <button type="submit" class="btn btn-danger btn-sm"><i style="font-size:24px" class="fa-solid fa-trash"></i></button>
  </form>
</template>

<script>
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
          console.log(this.postId, this.commentId);
          const response = await fetch(`/post/${this.postId}/comments/${this.commentId}/`, {
            method: 'POST',
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken'),
              'Content-Type': 'application/json',
            },
          });

          const data = await response.json();

          console.log(data);

          if (response.ok) {
            this.$emit('delete-comment', data);
          } else {
            console.error('Failed to delete comment');
          }
        } catch (error) {
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
  },
};
</script>