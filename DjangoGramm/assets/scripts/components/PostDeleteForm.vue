<template>
  <form @submit.prevent="submitForm" enctype="multipart/form-data" class="delete-form">
    <button type="submit" class="btn btn-outline-danger btn-form" :disabled="isSubmitting">
      <span v-if="!isSubmitting">Delete post</span>
        <span v-else class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </span>
    </button>
  </form>
</template>

<script>
  export default {
    data() {
      return {
        postId: initialData.id,
        isSubmitting: false,
      };
    },
    methods: {
      async submitForm() {
        this.isSubmitting = true;

        const formData = new FormData();
        formData.append('_method', 'DELETE');

        try {
          const response = await fetch(`/post/${this.postId}/update`, {
            method: 'POST',
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken'),
            },
            body: formData,
          });

          const data = await response.json();

          if (response.ok) {
            window.location.href = data.redirect_url;
          }
        } catch (error) {
          console.error('Error submitting form:', error);
        } finally {
          this.isSubmitting = false;
        }
      },
      getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      },
    },
  };
</script>